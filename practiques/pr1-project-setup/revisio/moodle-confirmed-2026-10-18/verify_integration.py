"""TIG-only integration checks. Mount no real submissions; use provider runtimes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

EDITION = Path(__file__).resolve().parent
ROOT = EDITION.parents[3]
MESA_IMAGE = "sha256:e4e0edeed0f159e5968f7435d32dc4eeb8b80c6b5071879b5952c4e12163867c"
WEB_IMAGE = "sha256:f0e7915527fa68a67448287e131ec431aeae902b8269856e4e219e67faade146"
PACKAGER_IMAGE = "sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546"
EXPECTED = "7c899db02195a75c76cb5217cfcab13fc5c017b4ae98ab99ddcc4b23dba09d1e"
PRIVATE_PATHS = [
    ".unaltramesa/private/identities.json",
    ".unaltramesa/private/pseudonym.key",
    ".unaltramesa/reports/teacher-workbook.ods",
    "assets/.unaltramesa/private/probe.json",
    "practiques/pr1-project-setup/revisio/.unaltramesa/private/probe.json",
    "sandbox/revisions/pr1-moodle/synthetic/run-01/originals/synthetic.pdf",
    "sandbox/revisions/pr1-moodle/synthetic/run-01/.unaltramesa/staging/stu-synthetic/notes.pdf",
    "sandbox/revisions/pr1-moodle/synthetic/run-01/.unaltramesa/reports/teacher-workbook.ods",
]

MESA_CHECK = r'''
from pathlib import Path
from io import BytesIO
import hashlib, json, os, sys, tempfile, zipfile
import xml.etree.ElementTree as ET
import pymupdf
from unaltramesa.activities import resolve_activity, activity_context, authoring_review_plan
from unaltramesa.inventory import inventory
from unaltramesa.recipe import load_recipe
from unaltramesa.checks import required_artifacts
from unaltramesa.runner import run_recipe
sys.path.insert(0, '/app/tests')
from test_qgis_pair import qgz_bytes, write_pair
source = Path('/activity-input')
profile = resolve_activity(source, edition='moodle-confirmed-2026-10-18', required_parts=['micropractice'])
plan = authoring_review_plan(profile)
assert [(c['id'], c['max_points']) for c in plan['criteria']] == [('BASIC', 70), ('EXTENSIONS', 20), ('DOCUMENTATION', 10)]
assert not any(c['agent_may_finalize'] for c in plan['criteria'])
try:
    resolve_activity(source, edition='wrong-edition', required_parts=['micropractice'])
except ValueError:
    pass
else:
    raise AssertionError('An incorrect edition was accepted')
with tempfile.TemporaryDirectory(prefix='tig-synthetic-') as tmp:
    root = Path(tmp)
    os.environ['MCP_CONSUMER_WORKSPACE'] = str(root)
    submission = root / 'stu-synthetic'
    submission.mkdir()
    # A deliberately different CRS and no layout: neither is an assigned requirement.
    with zipfile.ZipFile(BytesIO(qgz_bytes(crs='EPSG:4326', author='Synthetic Fixture'))) as archive:
        xml = ET.fromstring(archive.read('delivery.qgs'))
    xml.remove(xml.find('Layouts'))
    payload = BytesIO()
    with zipfile.ZipFile(payload, 'w') as archive:
        archive.writestr('delivery.qgs', ET.tostring(xml))
    write_pair(submission, payload.getvalue(), payload.getvalue())
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((40, 50), 'SYNTHETIC FIXTURE - PR1 QGIS WMS municipi')
    page.insert_text((40, 85), 'Select the municipality, export it and reopen the GeoPackage.')
    pdf.save(submission / 'notes.pdf')
    pdf.close()
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in submission.iterdir()}
    with activity_context(profile):
        recipe = load_recipe('tig-pr1-moodle-confirmed-2026-10-18')
        baseline = required_artifacts(recipe, inventory(submission))
        assert baseline['status'] == 'pass' and baseline['counts']['notes'] == 1
        result = run_recipe(recipe.id, submission, use_prepared_evidence=False)
        assert next(c for c in result['checks'] if c['check_id']=='submission.required_artifacts@1')['status']=='pass'
        assert all(hashlib.sha256((submission/name).read_bytes()).hexdigest()==value for name,value in before.items())
        (submission / 'optional-map.pdf').write_bytes((submission / 'notes.pdf').read_bytes())
        optional = required_artifacts(recipe, inventory(submission))
        assert optional['status'] == 'pass' and optional['counts']['notes'] == 2
        (submission / 'optional-map.pdf').unlink()
        (submission / 'notes.pdf').unlink()
        missing = required_artifacts(recipe, inventory(submission))
        assert missing['status'] == 'fail' and 'notes' in missing['summary']
    print(json.dumps({'ok':True,'effective_sha256':plan['effective_sha256'],
        'criteria':{c['id']:c['max_points'] for c in plan['criteria']},
        'one_notes_pdf_without_map':'pass','additional_pdf':'pass','missing_notes':'fail_as_expected',
        'wrong_edition':'rejected','checks_run':len(result['checks']),
        'input_bytes_preserved':True,'synthetic_crs':'EPSG:4326','composition_present':False,
        'limits':'Tests structural evidence and cardinalities; not geographic correctness, QGIS opening or visual grading.'}))
'''

WEB_CHECK = r'''
require 'jekyll'
require 'json'
config = Jekyll.configuration({'config'=>'/probe/_config.yml', 'source'=>'/probe/site',
  'destination'=>'/tmp/tig-site', 'cache_dir'=>'/tmp/tig-cache', 'disable_disk_cache'=>true,
  'theme'=>nil, 'plugins'=>[], 'quiet'=>true})
config['theme'] = nil
config['plugins'] = []
site = Jekyll::Site.new(config)
site.process
files = Dir.glob('/tmp/tig-site/**/*', File::FNM_DOTMATCH).select { |p| File.file?(p) }.map { |p| p.delete_prefix('/tmp/tig-site/') }
raise "Private probe leaked: #{files}" unless files == ['assets/public-probe.txt']
puts JSON.generate({'ok'=>true, 'jekyll'=>Jekyll::VERSION, 'published_files'=>files,
 'private_probes_excluded'=>JSON.parse(File.read('/probe/private-paths.json')).length,
 'scope'=>'Actual TIG exclusions with synthetic content; theme/plugins disabled for this isolated filter test.'})
'''

PACKAGE_CHECK = r'''
from pathlib import Path
from copy import deepcopy
import hashlib, json, os, tempfile, zipfile
from unaltraweb_mcp import practice_editions as editions
with tempfile.TemporaryDirectory(prefix='tig-package-synthetic-') as tmp:
    root = Path(tmp)
    safe = root/'payload/data/example.txt'
    safe.parent.mkdir(parents=True)
    safe.write_bytes(b'SYNTHETIC SELECTED TEACHING MATERIAL')
    for path in json.loads(Path('/probe/private-paths.json').read_text()):
        target = root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'SYNTHETIC PRIVATE STATE - NEVER DISTRIBUTE')
    # Also test private state adjacent to an explicitly selected product.
    (safe.parent/'.unaltramesa').mkdir()
    (safe.parent/'.unaltramesa/teacher-workbook.ods').write_bytes(b'SYNTHETIC PRIVATE STATE')
    row = {'id':'initial','path':str(safe.relative_to(root)),'sha256':hashlib.sha256(safe.read_bytes()).hexdigest(),
           'bytes':safe.stat().st_size,'role':'initial-data','kind':'output','ownership':'producer'}
    manifest = {'files':[row]}
    report = {'profile':'qgis-practice-v2','selected':['initial'],'closure':[{**row,'depends_on':[]}]}
    closure = editions.validate_closure(report, manifest, ['initial'], 'alumnat', profile='qgis-practice-v2')
    entries = [{'source':r['path'],'destination':r['path'],'sha256':r['sha256'],'bytes':r['bytes']} for r in closure]
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        editions.zip_files(root, fd, 'alumnat.zip', entries)
    finally:
        os.close(fd)
    with zipfile.ZipFile(root/'alumnat.zip') as archive:
        members = archive.namelist()
        assert members == [row['path']]
        assert b'PRIVATE STATE' not in archive.read(members[0])
    rejected = 0
    for role,kind in [('resolved-data','output'),('control','evidence'),('source','input')]:
        bad_manifest, bad_report = deepcopy(manifest), deepcopy(report)
        bad_manifest['files'][0].update(role=role,kind=kind)
        bad_report['closure'][0].update(role=role,kind=kind)
        try:
            editions.validate_closure(bad_report,bad_manifest,['initial'],'alumnat',profile='qgis-practice-v2')
        except ValueError:
            rejected += 1
    assert rejected == 3
    print(json.dumps({'ok':True,'archive_members':members,'unselected_private_state_excluded':True,
        'teacher_and_control_selections_rejected':rejected,
        'scope':'Unaltraweb explicit selection/closure and ZIP writer, using only synthetic files.'}))
'''


def run(*args, **kwargs):
    completed = subprocess.run(args, text=True, capture_output=True, timeout=180, **kwargs)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout


def container(image, mount_source, mount_target, entrypoint, code, *, environment=()):
    command = ['docker', 'run', '--rm', '--pull=never', '--network', 'none', '--read-only',
               '--tmpfs', '/tmp:rw,nosuid,nodev,size=512m', '--memory', '1g', '--cpus', '2',
               '--pids-limit', '256', '--user', f'{os.getuid()}:{os.getgid()}', '--security-opt', 'no-new-privileges', '--cap-drop', 'ALL',
               '--mount', f'type=bind,src={mount_source},dst={mount_target},readonly']
    for value in environment:
        command += ['--env', value]
    command += ['--entrypoint', entrypoint, image, '-e' if entrypoint == 'ruby' else '-c', code]
    output = run(*command)
    return json.loads(output.strip().splitlines()[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    assert Path(run('git', 'rev-parse', '--show-toplevel', cwd=ROOT).strip()) == ROOT
    imported = json.loads((EDITION/'import-manifest.json').read_text())
    for name, digest in imported['files'].items():
        assert hashlib.sha256((EDITION/name).read_bytes()).hexdigest() == digest, name
    private = '\n'.join(PRIVATE_PATHS) + '\n'
    ignored = run('git', 'check-ignore', '--no-index', '--stdin', input=private, cwd=ROOT).splitlines()
    assert ignored == PRIVATE_PATHS
    ignore_details = run('git', 'check-ignore', '--no-index', '--verbose', '--stdin',
                         input=private, cwd=ROOT).splitlines()
    patterns = {}
    for detail in ignore_details:
        rule, path = detail.split('\t', 1)
        source, _, pattern = rule.split(':', 2)
        assert source == '.gitignore', 'Private state must be excluded by repository rules'
        patterns[path] = pattern
    tracked = run('git', 'ls-files', '-z', '--', 'sandbox', '.unaltramesa', ':(glob)**/.unaltramesa/**', cwd=ROOT)
    assert not tracked, 'Private assessment state is tracked'
    definition_files = '\n'.join(str((EDITION/name).relative_to(ROOT)) for name in imported['files'])+'\n'
    probe = subprocess.run(['git','check-ignore','--no-index','--stdin'],input=definition_files,
                           text=True,capture_output=True,cwd=ROOT,timeout=10)
    assert probe.returncode == 1 and not probe.stdout, 'Definition is incorrectly ignored'
    mesa = container(MESA_IMAGE, EDITION, '/activity-input', 'python', MESA_CHECK)
    assert mesa['effective_sha256'] == EXPECTED
    with tempfile.TemporaryDirectory(prefix='tig-review-integration-') as temporary:
        fixture = Path(temporary)
        shutil.copyfile(ROOT/'_config.yml', fixture/'_config.yml')
        public = fixture/'site/assets/public-probe.txt'
        public.parent.mkdir(parents=True)
        public.write_text('SYNTHETIC PUBLIC CONTROL\n')
        paths = PRIVATE_PATHS + ['practiques/pr1-project-setup/revisio/moodle-confirmed-2026-10-18/rubric.yml',
                                 'dist/practiques/teacher-workbook.ods']
        (fixture/'private-paths.json').write_text(json.dumps(paths))
        for path in paths:
            p = fixture/'site'/path
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('SYNTHETIC PRIVATE STATE\n')
        web = container(WEB_IMAGE, fixture, '/probe', 'ruby', WEB_CHECK)
        packaging = container(PACKAGER_IMAGE, fixture, '/probe', 'python3', PACKAGE_CHECK,
                              environment=('PYTHONPATH=/opt/unaltraweb/src',))
    hashes = {'_config.yml':hashlib.sha256((ROOT/'_config.yml').read_bytes()).hexdigest()}
    result = {'schema_version':1,'kind':'tig-review-integration-validation','ok':True,
              'activity':'tig/pr1-moodle','edition':'moodle-confirmed-2026-10-18',
              'real_submissions_used':False,'real_privacy_approval':False,
              'imported_bytes_verified':len(imported['files']),
              'runtime_images':{'unaltramesa':MESA_IMAGE,'jekyll':WEB_IMAGE,'practice_packager':PACKAGER_IMAGE},
              'definition_and_synthetic_checks':mesa,'git':{'private_paths_ignored':len(ignored),
              'private_state_tracked':False,'definition_versionable':True,'applied_patterns':patterns},'web':web,'student_package':packaging,
              'input_sha256':hashes,
              'verification_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.write_report:
        (EDITION/'integration-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
