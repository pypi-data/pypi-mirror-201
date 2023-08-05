from __future__ import annotations

import abc
import json
import pathlib
from typing import Iterable, Optional

from typing_extensions import Literal
import np_logging

from np_session.session import Session
from np_session.components import SettingsXmlInfo, settings_xml_info_from_path
import np_session.databases.sql_alchemy as db

logger = np_logging.getLogger()

class Dumper(abc.ABC):
    
    probe_letter_to_metrics_csv: dict[str, pathlib.Path]
    probe_serial_number_to_metrics_csv: dict[int, pathlib.Path]
    
    rig: Optional[Literal['NP.0', 'NP.1', 'NP.2', 'NP.3', 'NP.4']] = None
    
    settings_xml_info: Optional[SettingsXmlInfo] = None
    """"Contains probe serial numbers and other recording metadata (datetime, hostname,
    OpenEphys version).
    
    If not available, probe serial numbers can possibly be obtained from `probe_info.json`.
    """
    
    @abc.abstractmethod
    def to_db(self, overwrite_existing: bool) -> None: ...
    
    @property
    def probe_serial_number_to_letter(self) -> dict[int, str | None]:
        if self.settings_xml_info:
            return dict(zip(self.settings_xml_info.probe_serial_numbers, self.settings_xml_info.probe_letters))
        metrics_csv_to_probe_letter = {v: k for k, v in self.probe_letter_to_metrics_csv.items()}
        return {k: metrics_csv_to_probe_letter[v] for k, v in self.probe_serial_number_to_metrics_csv.items()}
    
class WithLims(Dumper):    
    
    def __init__(self, session: str | pathlib.Path | Session) -> None:
        self.session = Session(session) if not isinstance(session, Session) else session
        
        
class SqlAlchemy(WithLims, Dumper):
    
    def __init__(self, session: str | pathlib.Path | Session) -> None:
        
        super().__init__(session)
        
        self.probe_letter_to_metrics_csv = self.session.probe_letter_to_metrics_csv_path
        
        settings_xml_path = self.session.find_settings_xml()
        if settings_xml_path:
            self.settings_xml_info = settings_xml_info_from_path(settings_xml_path)

        self.probe_serial_number_to_metrics_csv = {
            serial_number: self.probe_letter_to_metrics_csv[letter]
            for serial_number, letter in self.probe_serial_number_to_letter.items() if letter
        }
        rig = self.session.rig
        
    def to_db(self, overwrite_existing=True) -> None:
        
        lims = db.LIMSEcephysSession(lims_id=self.session.id)
        
        probe_types = db.Probe.NeuropixelsVersion.enums
        
        if not self.settings_xml_info:
            raise ValueError(f'No settings.xml available: {self.session!r}')
            # it might be possible to get probe serial numbers from probe_info.json and
            # creae recordings that aren't joined by settings_xml_md5
        
        xml = self.settings_xml_info
        
        rec = db.Recording(
            settings_xml_md5=xml.settings_xml_md5,
            lims_session_id=self.session.id,
            hostname=xml.hostname,
            rig=self.rig.id if self.rig else None,
            date=xml.date,
            start_time=xml.start_time,
            open_ephys_version=xml.open_ephys_version,
        )
        
        probes = []
        for serial_number, np_type in zip(xml.probe_serial_numbers, xml.probe_types):
            probes.append(
                db.Probe(
                    serial_number=serial_number,
                    neuropixels_version=next((_ for _ in probe_types if _ in np_type), 'unknown'),
                )
            )
        
        sorted_probes = []
        for serial_number, letter in self.probe_serial_number_to_letter.items():
            sorted_probes.append(
                db.SortedProbeRecording(
                    settings_xml_md5=xml.settings_xml_md5,
                    probe_serial_number=serial_number,
                    probe_letter=letter,
                    metrics_csv_md5=db.md5(self.probe_serial_number_to_metrics_csv[serial_number]),
                )
            )
        
        sorted_units = [
            db.SortedUnit.units_from_csv_path(
                csv_path,       
            ) for csv_path in self.probe_serial_number_to_metrics_csv.values()
        ]
        with db.SESSION.no_autoflush as session:
            
            if overwrite_existing:
                write = session.merge
            else:
                write = session.add
                
            write(lims)
            write(rec)
            
            def rec_write(iterable: Iterable):
                if not isinstance(iterable, Iterable):
                    write(iterable)
                else:
                    for _ in iterable:
                        rec_write(_)
                        
            for _ in (probes, sorted_probes, sorted_units):
                rec_write(_)
            session.commit()
            
if __name__ == '__main__':
    # d = SqlAlchemy('c:/1116941914_surface-image1-left.png')
    # d.to_db()
    # stmt = db.select(db.Probe)#.where(db.Probe.serial_number.in_([18005117142]))

    # for probe in db.SESSION.scalars(stmt):
    #     print(probe)
    # # df = pd.read_sql_table('sorted_probe_recordings', db.ENGINE)
    idx =0
    for session in json.loads(pathlib.Path('sessions.json').read_bytes()):
        # try:
        logger.info(f'Adding {session} to db...')
        d = SqlAlchemy(session)
        d.to_db()
        idx += 1
        # if idx == 3:
        #     break
        # except Exception as exc:
        #     logger.exception(exc)
            
    