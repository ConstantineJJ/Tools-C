"""Discovery/search behavior, independent of Blender and the MCP SDK."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

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


if __name__=='__main__': unittest.main()
