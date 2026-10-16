"""Discovery/search behavior, independent of Blender and the MCP SDK."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check
import skill_catalog


class SkillCatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='skill catalog ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root/'docs').mkdir()
        (self.root/'docs/foundation.md').write_text('Only foundation contains outsideword.\n')
        self.manifest = dict(schema_version=1, version='4.0.3', skills=[], blender_aliases={})
        for name, description, body in [
            ('hair-model', 'Develop hair geometry and controlled shapes.', 'Unique strandneedle recipe.'),
            ('surface-work', 'Finish material surfaces.', 'hair '*400 + 'Surface recipe.')]:
            path='skills/'+name+'/SKILL.md'
            target=self.root/path
            target.parent.mkdir(parents=True)
            target.write_text('---\nname: '+name+'\ndescription: '+description+'\n---\n# '+name+'\n'
                              '[foundation](../../docs/foundation.md)\n'+body+'\n## Pitfalls / Lessons Learned\n',encoding='utf-8')
            self.manifest['skills'].append(dict(id=name,path=path))
        self.manifest['blender_aliases']['Legacy_Hair']=dict(reference='skills/hair-model/SKILL.md',source_sha256='0'*64,source_version='1')
        (self.root/'AGENTS.md').write_text('\n'.join(r['path'] for r in self.manifest['skills']))
        (self.root/'docs/skills.md').write_text('\n'.join(
            '['+r['id']+'](../'+r['path']+')' for r in self.manifest['skills']))
        self.write_manifest()

    def write_manifest(self):
        (self.root/'manifest.json').write_text(json.dumps(self.manifest),encoding='utf-8')

    def test_canonical_owners_and_aliases_are_separate_without_expanded_bodies(self):
        result=skill_catalog.listing(self.root)
        self.assertEqual(result['canonical_count'],2)
        self.assertEqual(len(result['compatibility_aliases']),1)
        self.assertEqual(result['canonical_skills'][0]['aliases'],['Legacy_Hair'])
        self.assertTrue(all('content' not in r for r in result['canonical_skills']))

    def test_precise_owner_ids_and_legacy_aliases_find_the_same_readable_owner(self):
        for query in ['hair-model','HAIR-MODEL','Legacy_Hair']:
            with self.subTest(query=query):
                result=skill_catalog.search(self.root,query)
                self.assertEqual([r['name'] for r in result['results']],['hair-model'])
                self.assertEqual(result['search_scope'],'metadata')

    def test_repeated_unrelated_body_terms_do_not_outweigh_owner_purpose(self):
        result=skill_catalog.search(self.root,'hair')
        self.assertEqual([r['name'] for r in result['results']],['hair-model'])
        self.assertLess(len(result['results'][0]['excerpt']),750)

    def test_owner_name_beats_a_secondary_exclusion_in_another_description(self):
        path=self.root/'skills/surface-work/SKILL.md'
        path.write_text(path.read_text().replace('Finish material surfaces.', 'Finish material surfaces; hair geometry belongs elsewhere.'))
        result=skill_catalog.search(self.root,'hair')
        self.assertEqual([r['name'] for r in result['results']],['hair-model'])

    def test_entrypoint_fallback_finds_a_recipe_without_expanding_dependencies(self):
        result=skill_catalog.search(self.root,'strandneedle')
        self.assertEqual(result['search_scope'],'entrypoint')
        self.assertEqual(result['results'][0]['name'],'hair-model')
        self.assertIn('strandneedle',result['results'][0]['excerpt'])
        self.assertEqual(skill_catalog.search(self.root,'outsideword')['count'],0)

    def test_discovery_limits_and_invalid_queries_are_bounded(self):
        self.assertEqual(skill_catalog.search(self.root,'geometry material',1)['count'],1)
        self.assertEqual(skill_catalog.search(self.root,'geometry material',0)['count'],1)
        self.assertEqual(skill_catalog.search(self.root,'geometry material',1000)['count'],2)
        for query in ['', ' ', '...']:
            self.assertFalse(skill_catalog.search(self.root,query)['ok'])

    def test_edited_canonical_metadata_is_visible_on_the_next_request(self):
        path=self.root/'skills/hair-model/SKILL.md'
        self.assertEqual(skill_catalog.search(self.root,'featherneedle')['count'],0)
        path.write_text(path.read_text().replace('Develop hair geometry','Develop featherneedle geometry'))
        self.assertEqual(skill_catalog.search(self.root,'featherneedle')['results'][0]['name'],'hair-model')

    def test_untrusted_catalog_paths_cannot_escape_the_canonical_root(self):
        self.manifest['skills'][0]['path']='../foreign/SKILL.md'
        self.write_manifest()
        with self.assertRaises(check.Violation):
            skill_catalog.listing(self.root)

    def test_real_catalog_covers_owners_missing_from_legacy_discovery(self):
        result=skill_catalog.listing(check.ROOT)
        expected={r['id'] for r in check.catalog(check.ROOT)['skills']}
        self.assertEqual({r['name'] for r in result['canonical_skills']},expected)
        self.assertEqual(len(result['compatibility_aliases']),9)
        for owner in ['blender-anime-character-modeling','blender-vegetation','blender-props']:
            self.assertEqual(skill_catalog.search(check.ROOT,owner)['results'][0]['name'],owner)
        self.assertEqual([r['name'] for r in skill_catalog.search(check.ROOT,'vegetation')['results']],['blender-vegetation'])

    def test_listing_does_not_read_complete_skills_or_supporting_references(self):
        original = Path.read_text
        def guarded(path, *args, **kwargs):
            if path.name != 'manifest.json':
                raise AssertionError('Metadata listing read a full document: '+str(path))
            return original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', guarded):
            self.assertEqual(skill_catalog.listing(self.root)['canonical_count'], 2)

    def test_equal_size_timestamp_metadata_edit_is_not_cached(self):
        import os
        path = self.root/'skills/hair-model/SKILL.md'
        skill_catalog.listing(self.root)
        stamp = path.stat()
        path.write_text(path.read_text().replace('Develop', 'Prepare'), encoding='utf-8')
        os.utime(path, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
        self.assertTrue(skill_catalog.listing(self.root)['canonical_skills'][0]['description'].startswith('Prepare'))

    def test_audit_discovery_matrix_and_all_explicit_names(self):
        import mcp_runtime as runtime
        matrix = check.read_json(check.ROOT/'tests/skill_behavior_cases.json')
        for case in matrix['discovery']:
            with self.subTest(case=case['id']):
                self.assertEqual(runtime.route_task(case['query']), case['owners'])
                found = skill_catalog.search(check.ROOT, case['query'])
                self.assertEqual([r['name'] for r in found['results']], case.get('search_owners', case['owners']))
        for row in skill_catalog.listing(check.ROOT)['canonical_skills']:
            self.assertEqual(runtime.route_task(row['name']), [row['name']])

    def test_duplicate_manifest_ids_and_header_names_fail_closed(self):
        self.manifest['skills'].append(self.manifest['skills'][0].copy())
        self.write_manifest()
        with self.assertRaises(check.Violation): skill_catalog.listing(self.root)
        self.manifest['skills'].pop(); self.write_manifest()
        path=self.root/'skills/hair-model/SKILL.md'
        path.write_text(path.read_text().replace('name: hair-model','name: other'))
        with self.assertRaises(check.Violation): skill_catalog.listing(self.root)

    def test_preservation_does_not_swallow_authorized_neighboring_action(self):
        import mcp_runtime as runtime
        self.assertEqual(runtime.route_task('Проверь модель, исправь веса, существующие анимации сохранить'),
                         ['verification','blender-rigging-skinning'])
        self.assertEqual(runtime.route_task('Animation looks wrong; fix shoulder weights.'),
                         ['verification','blender-rigging-skinning'])

    def test_warm_process_uses_current_resolver_without_restarting_mcp(self):
        import mcp_runtime as runtime
        with patch.object(check, 'catalog_manifest', None), patch.object(runtime, 'route_task', side_effect=AssertionError('cached router used')):
            self.assertEqual([r['name'] for r in skill_catalog.search(check.ROOT,'Model a human head from reference')['results']],
                             ['visual-reference-reconstruction','blender-character-modeling'])

    def test_generic_context_does_not_inherit_blender_wrapper(self):
        import mcp_runtime as runtime
        result=runtime.context(check.ROOT,'project-audit')
        self.assertTrue(result['ok'])
        self.assertNotIn('SOURCE: docs/blender-evidence.md',result['skills'][0]['content'])

    def test_explicit_long_stage_sequence_loads_only_current_phase(self):
        import mcp_runtime as runtime
        q='Create a character, then create a rig, then create animation, then export GLB.'
        expected=['blender-character-modeling','blender-rigging-skinning','blender-animation','blender-export-validation']
        self.assertEqual(runtime.route_task(q),expected)
        result=runtime.context(check.ROOT,q)
        self.assertTrue(result['ok'])
        self.assertEqual([r['name'] for r in result['skills']],expected[:1])
        self.assertEqual(result['routing']['deferred_owners'],expected[1:])
        self.assertNotIn('SOURCE: skills/blender-animation/SKILL.md',result['skills'][0]['content'])
        self.assertTrue(all(row['status']=='DISCOVERED' for row in result['skill_usage']))


if __name__=='__main__': unittest.main()
