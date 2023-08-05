from __future__ import annotations

import json
import pathlib
import pprint
from typing import Optional

import np_logging

import np_session.session

from np_session.components.paths import INCOMING_ROOT as DEFAULT_INCOMING_ROOT

logger = np_logging.getLogger(__name__)

def get_files(  
    session: Optional[str | pathlib.Path | np_session.session.Session] = None,
    files: Optional[dict] = None,
    platform_json: Optional[pathlib.Path] = None,
) -> list[pathlib.Path]:
    """By default, gets paths for the files in the platform D1 json on npexp for the Session provided."""
    if session and not (files or platform_json): # if session is provided, use it to get the platform json
        if not isinstance(session, np_session.session.Session):
            session = np_session.session.Session(session)
    platform_json = next(session.npexp_path.glob('*platformD1*.json'), None)
      
    if not platform_json:
        raise ValueError("No platform json provided or found in npexp")
    
    if files:
        files = files.get("files", files)
    else:
        files = json.loads(platform_json.read_bytes()).get("files")
    
    if not files:
        raise ValueError(f"No files provided or found in {platform_json}")
    
    logger.info('Return paths for files in %s', platform_json.parent)
    return [platform_json.parent / tuple(file.values())[0] for file in files.values()]

def check_files(
    session: Optional[str | pathlib.Path | np_session.session.Session] = None,
    files: Optional[dict] = None,
    platform_json: Optional[pathlib.Path] = None,
    ) -> list[tuple[pathlib.Path, bool]]:
    """By default, checks the platform D1 json on npexp for the Session provided."""
    paths = get_files(session, files, platform_json)
    results = sorted([(p, p.exists()) for p in paths if p.exists()], key=lambda x: x[0].name) 
    results.extend(sorted([(p, p.exists()) for p in paths if not p.exists()], key=lambda x: x[0].name))
    pprint.pprint([f'{r[0].name} exists: {r[1]}' for r in results])
    return results

def write_trigger_file(
    session: np_session.session.Session, 
    incoming_dir: pathlib.Path = DEFAULT_INCOMING_ROOT,
    trigger_dir: pathlib.Path = DEFAULT_INCOMING_ROOT / "trigger",
    override: bool = False,
    ) -> None:
    """Write a trigger file to initiate ecephys session data upload to lims.
    
    - designated "incoming" folders have a `trigger` dir which is scanned periodically for trigger files
    - a trigger file provides:
        - a lims session ID 
        - a path to an "incoming" folder where new session data is located, ready for
          upload
            - this path is typically the parent of the trigger dir, where lims has
              read/write access for deleting session data after upload, but it can be
              anywhere on //allen
        - once the trigger file is detected, lims searches for a file in the incoming
          dir named '*platform*.json', which should contain a `files` dict
    """
    if not incoming_dir.exists():
        logger.warning("Incoming dir doesn't exist or isn't accessible - lims upload job will fail when triggered: %s", incoming_dir)
    elif not tuple(incoming_dir.glob(f"*{session.id}*platform*.json")):
        logger.warning("No platform json found for %s in incoming dir - lims upload job will fail when triggered: %s", session.id, incoming_dir)
        
    trigger_file = pathlib.Path(trigger_dir / f"{session.id}.ecp")
    trigger_file.touch()    
    # don't mkdir for trigger_dir or parents 
    # - doesn't make sense to create, since it's a dir lims needs to know about and
    #   be set up to monitor
    # - if it doesn't exist or is badly specified, the file
    #   operation should raise the appropriate error 
    
    contents = (
        f"sessionid: {session.id}\n"
        f"location: '{incoming_dir.as_posix()}'"
    )
    trigger_file.write_text(contents)
        
    logger.info("Trigger file written for %s in %s:\n%s", session, trigger_file.parent, trigger_file.read_text())