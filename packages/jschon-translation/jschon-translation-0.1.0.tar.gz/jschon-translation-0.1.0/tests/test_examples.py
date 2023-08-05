import pathlib
from datetime import datetime
from urllib.parse import urlparse

from jschon import JSON, JSONSchema
from jschon.jsonpatch import JSONPatch
from jschon_translation import translation_filter

examples_dir = pathlib.Path(__file__).parent.parent / 'jschon_translation' / 'json-translation-vocabulary' / 'examples'


@translation_filter('date-to-year')
def date_to_year(date: str) -> int:
    return datetime.strptime(date, '%Y-%m-%d').year


@translation_filter('base-url')
def base_url(url: str) -> str:
    u = urlparse(url)
    return f'{u.scheme}://{u.netloc}'


def test_translate_iso19115_to_datacite():
    example_dir = examples_dir / 'iso19115-to-datacite'
    input_schema = JSONSchema.loadf(example_dir / 'input-schema.json')
    input_json = JSON.loadf(example_dir / 'input.json')
    output_schema = JSONSchema.loadf(example_dir / 'output-schema.json')
    output_json = JSON.loadf(example_dir / 'output.json')

    # sanity checks
    assert input_schema.validate().valid
    assert input_schema.evaluate(input_json).valid
    assert output_schema.validate().valid
    assert output_schema.evaluate(output_json).valid

    result = input_schema.evaluate(input_json)
    patch = result.output('translation-patch', scheme='datacite')
    translation = result.output('translation', scheme='datacite', clear_empties=False)
    assert JSONPatch(*patch).evaluate(None) == translation
    translation = result.output('translation', scheme='datacite', clear_empties=True)
    assert translation == output_json
