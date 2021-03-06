from pprint import pprint
import itertools
import pytest
import json
import en_core_web_sm
import en_core_sci_sm
from spacy.tokens import Token
from role_pattern_nlp import RolePatternBuilder, RolePatternSet
from role_pattern_nlp.exceptions import FeaturesNotInFeatureDictError
from role_pattern_nlp import util
import visualise_spacy_tree


idxs_to_tokens = util.idxs_to_tokens
# nlp = en_core_web_sm.load()
nlp = en_core_sci_sm.load()
Token.set_extension('valence', default=False)
Token.set_extension('has_valence', default=False)


text1 = 'We introduce efficient methods for fitting Boolean models to molecular data, successfully demonstrating their application to synthetic time courses generated by a number of established clock models, as well as experimental expression levels measured using luciferase imaging.'

text2 = 'The amyloid-beta oligomer hypothesis was introduced in 1998.'

text3 = 'L-theanine alone improved self-reported relaxation, tension, and calmness starting at 200 mg.'

text4 = 'These include maintaining a consistent bedtime routine, establishing healthy eating habits and exercise, avoiding caffeine and other substances that can exacerbate RLS, and stretching before bedtime.'

text5 = 'Smoking and heavy alcohol consumption were associated with increased risks.'

text6 = 'In both CC and AA adults, greater adherence to a Prudent dietary pattern was associated with better cognitive outcomes.'

text7 = 'However, expectancy and the related psychological permutations that are associated with oral CAF ingestion are generally not considered in most experimental designs and these could be important in understanding if/how CAF elicits an ergogenic effect.'

text8 = 'Epigallocatechin-3-gallate (EGCG), the most abundant catechin found in green tea, has been associated with potential health benefits, both on cognition and cardiovascular phenotypes, through several mechanisms.'

text9 = 'Current cigarette smoking was associated with faster cognitive decline (hazard ratio, 3.20; 95% confidence interval, 1.02-10.01).'

text10 = 'The flavonoid quercetin and the stilbene resveratrol have also been associated with cardiometabolic health.'

text11 = 'A battery of attentional and working memory measures was completed at baseline then 45, 90 and 180 min post-treatment.'

text12 = 'RPE was assessed at 10-min intervals during exercise.'

text13 = (
    'The number of passing the target was significantly reduced in those offspring.'
)

text14 = 'L-theanine, caffeine and the combination decreased task-related fMRI reactivity of the default mode network in the brain, which is known to show increased activity during mind wandering.'

text15 = 'SRE feeding significantly prevented cognitive decline, whereas YBE feeding had little effect.'

text16 = 'Decaffeinated coffee also increased alertness when compared to placebo.'

text17 = 'However, even the smallest number exceeded the standard number for drinking beverages.'

text18 = 'This study determined chronic influence of prenatal caffeine at relatively higher doses on cognitive functions in the rat offspring.'

text19 = 'Caffeine readministration alleviated all withdrawal symptoms and cognitive decrements within 45 min.'

text20 = 'In addition to the previous data demonstrating that valproic acid can upregulate NEP expression both in neuroblastoma cells and in rat Cx and Hip we have further confirmed that caspase inhibitors can also restore NEP expression in rat Cx reduced after prenatal hypoxia.'

text21 = 'Results revealed that adjunctive L-theanine did not outperform placebo for anxiety reduction on the HAMA (p=0.73) nor insomnia severity on the Insomnia Severity Index (ISI; p=0.35).'

text22 = 'The results highlight a beneficial effect of nutritional supplements on information processing and RPE.'

text23 = 'We also discuss the applied relevance of our results as coffee and tea are among the most prevalent beverages globally.'

doc1 = nlp(text1)
doc2 = nlp(text2)
doc3 = nlp(text3)
doc4 = nlp(text4)
doc5 = nlp(text5)
doc6 = nlp(text6)
doc7 = nlp(text7)
doc8 = nlp(text8)
doc9 = nlp(text9)
doc10 = nlp(text10)
doc11 = nlp(text11)
doc12 = nlp(text12)
doc13 = nlp(text13)
doc14 = nlp(text14)
doc15 = nlp(text15)
doc16 = nlp(text16)
doc17 = nlp(text17)
doc18 = nlp(text18)
doc19 = nlp(text19)
doc20 = nlp(text20)
doc21 = nlp(text21)
doc22 = nlp(text22)
doc23 = nlp(text23)

doc14[6]._.set('valence', 'DOWN')
doc15[3]._.set('valence', 'DOWN')
doc16[3]._.set('valence', 'UP')
doc20[11]._.set('valence', 'UP')
doc14[6]._.set('has_valence', True)
doc15[3]._.set('has_valence', True)
doc16[3]._.set('has_valence', True)
doc20[11]._.set('has_valence', True)


docs = [
    doc1,
    doc2,
    doc3,
    doc4,
    doc5,
    doc6,
    doc7,
    doc8,
    doc9,
    doc10,
    doc11,
    doc12,
    doc13,
    doc14,
    doc15,
    doc16,
    doc17,
    doc18,
    doc19,
    doc20,
    doc21,
    doc22,
    doc23,
]


cases = [
    {
        'training_example': {
            'doc': doc1,
            'match': {
                'slot1': idxs_to_tokens(doc1, [0]),  # [We]
                'slot2': idxs_to_tokens(doc1, [1]),  # [introduce]
                'slot3': idxs_to_tokens(doc1, [3]),  # [methods]
            },
        }
    },
    {
        'training_example': {
            'doc': doc1,
            'match': {
                'slot1': idxs_to_tokens(doc1, [13, 15]),  # [demonstrating, application]
                'slot2': idxs_to_tokens(doc1, [16, 19]),  # [to, courses]
            },
        }
    },
    {
        'training_example': {
            'doc': doc1,
            'match': {
                'arg1': idxs_to_tokens(doc1, [19]),  # [courses]
                'pred': idxs_to_tokens(doc1, [20, 21]),  # [generated, by]
                'arg2': idxs_to_tokens(doc1, [27]),  # [models]
            },
        }
    },
    {
        'training_example': {
            'doc': doc3,
            'match': {
                'ant': idxs_to_tokens(doc3, [2]),  # [theanine]
                'cons': idxs_to_tokens(doc3, [8]),  # [relaxation]
            },
        }
    },
    {
        'training_example': {
            'doc': doc4,
            'match': {
                'ant': idxs_to_tokens(doc4, [16]),  # [caffeine]
                'cons': idxs_to_tokens(doc4, [23]),  # [RLS]
            },
        }
    },
    {
        'training_example': {
            'doc': doc6,
            'match': {
                'assoc_left': idxs_to_tokens(doc6, [8]),  # [adherence]
                'assoc_right': idxs_to_tokens(doc6, [19]),  # [outcomes]
            },
        },
        'pos_examples': [
            {
                'doc': doc8,
                'match': {
                    'assoc_left': idxs_to_tokens(
                        doc8, [0]
                    ),  # [Epigallocatechin-3-gallate]
                    'assoc_right': idxs_to_tokens(doc8, [20]),  # [benefits]
                },
            }
        ],
        'neg_examples': [
            {
                'doc': doc7,
                'match': {
                    'assoc_left': idxs_to_tokens(doc7, [2]),  # [expectancy]
                    'assoc_right': idxs_to_tokens(doc7, [22]),  # [designs]
                },
            },
            {
                'doc': doc8,
                'match': {
                    'assoc_left': idxs_to_tokens(
                        doc8, [0]
                    ),  # [Epigallocatechin-3-gallate]
                    'assoc_right': idxs_to_tokens(doc8, [31]),  # [mechanisms]
                },
            },
        ],
    },
    {
        'training_example': {
            'doc': doc9,
            'match': {
                'assoc_left': idxs_to_tokens(doc9, [2]),  # [smoking]
                'assoc_right': idxs_to_tokens(doc9, [8]),  # [decline]
            },
        },
        'pos_examples': [
            {
                'doc': doc10,
                'match': {
                    'assoc_left': idxs_to_tokens(doc10, [2]),  # [quercetin]
                    'assoc_right': idxs_to_tokens(doc10, [13]),  # [health]
                },
            }
        ],
        'neg_examples': [
            {
                'doc': doc8,
                'match': {
                    'assoc_left': idxs_to_tokens(
                        doc8, [0]
                    ),  # [Epigallocatechin-3-gallate]
                    'assoc_right': idxs_to_tokens(doc8, [24]),  # [cognition]
                },
            },
            {
                'doc': doc11,
                'match': {
                    'assoc_left': idxs_to_tokens(doc11, [1]),  # [battery]
                    'assoc_right': idxs_to_tokens(doc11, [11]),  # [baseline]
                },
            },
            {
                'doc': doc12,
                'match': {
                    'assoc_left': idxs_to_tokens(doc12, [0]),  # [RPE]
                    'assoc_right': idxs_to_tokens(doc12, [7]),  # [exercise]
                },
            },
            {
                'doc': doc13,
                'match': {
                    'assoc_left': idxs_to_tokens(doc13, [1]),  # [number]
                    'assoc_right': idxs_to_tokens(doc13, [11]),  # [offspring]
                },
            },
        ],
    },
    {
        'training_example': {
            'doc': doc14,
            'match': {
                'ant': idxs_to_tokens(doc14, [0]),  # [L-theanine]
                'cons': idxs_to_tokens(doc14, [9]),  # [reactivity]
            },
        },
        'pos_examples': [
            {
                'doc': doc15,
                'match': {
                    'ant': idxs_to_tokens(doc15, [0]),  # [SRE]
                    'cons': idxs_to_tokens(doc15, [5]),  # [decline]
                },
            },
            {
                'doc': doc16,
                'match': {
                    'ant': idxs_to_tokens(doc16, [1]),  # [coffee]
                    'cons': idxs_to_tokens(doc16, [4]),  # [alertness]
                },
            },
        ],
        'neg_examples': [
            {
                'doc': doc17,
                'match': {
                    'ant': idxs_to_tokens(doc17, [5]),  # [number]
                    'cons': idxs_to_tokens(doc17, [9]),  # [number]
                },
            },
            {
                'doc': doc18,
                'match': {
                    'ant': idxs_to_tokens(doc18, [1]),  # [study]
                    'cons': idxs_to_tokens(doc18, [4]),  # [influence]
                },
            },
        ],
    },
    {
        'training_example': {
            'doc': doc20,
            'match': {
                'ant': idxs_to_tokens(doc20, [9]),  # [acid]
                'cons': idxs_to_tokens(doc20, [13]),  # [expression]
            },
        },
        'neg_examples': [
            {
                'doc': doc21,
                'match': {
                    'ant': idxs_to_tokens(doc21, [4]),  # [L-theanine]
                    'cons': idxs_to_tokens(doc21, [8]),  # [placebo]
                },
            }
        ],
    },
    {
        'training_example': {
            'doc': doc22,
            'match': {
                'ant': idxs_to_tokens(doc22, [8]),  # [supplements]
                'cons': idxs_to_tokens(doc22, [13]),  # [RPE]
            }
        },
        'neg_examples': [
            {
                'doc': doc23,
                'match': {
                    'ant': idxs_to_tokens(doc23, [8]),  # [results]
                    'cons': idxs_to_tokens(doc23, [12]),  # [tea]
                },
            }
        ],
    }
]


feature_combs = [['DEP', 'TAG', 'LOWER'], ['DEP', 'TAG'], ['DEP']]


def test_build_pattern_and_find_matches():
    feature_dict = {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'}
    for case in cases:
        doc = case['training_example']['doc']
        match_example = case['training_example']['match']
        role_pattern_builder = RolePatternBuilder(feature_dict)
        for features in feature_combs:
            role_pattern = role_pattern_builder.build(
                match_example, features=features, validate_pattern=True
            )
            matches = role_pattern.match(doc)
            assert match_example in matches, 'does not match example'
            # print('passed')


def test_with_custom_extensions():
    doc4[22]._.set('valence', 'UP')
    feature_dict = {'DEP': 'dep_', '_': {'valence': 'valence'}}
    case = {
        'training_example': {
            'doc': doc4,
            'match': {
                'head': idxs_to_tokens(doc4, [23]),  # [RLS]
                'up': idxs_to_tokens(doc4, [22]),  # [exacerbate]
            },
        }
    }
    doc = case['training_example']['doc']
    match_example = case['training_example']['match']
    # pprint(match_example)
    role_pattern_builder = RolePatternBuilder(feature_dict)
    role_pattern = role_pattern_builder.build(match_example, validate_pattern=False)
    matches = role_pattern.match(doc)
    assert match_example in matches, 'does not match example'
    # print('passed')


def test_refine_pattern():
    refine_cases = [case for case in cases if 'neg_examples' in case]
    for case_i, case in enumerate(refine_cases):
        training_match = case['training_example']['match']
        neg_examples = case['neg_examples']
        feature_dicts = [
            {'DEP': 'dep_', 'TAG': 'tag_'},
            {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'},
            {'DEP': 'dep_', 'TAG': 'tag_', '_': {'has_valence': 'has_valence'}},
            # {'DEP': 'dep_', 'TAG': 'tag_', '_': {'valence': 'valence'}},
        ]
        role_pattern_builder = RolePatternBuilder(feature_dicts[0])
        pattern = role_pattern_builder.build(training_match, features=['DEP', 'TAG'])
        matches = [pattern.match(d) for d in docs]
        matches = util.flatten_list(matches)
        assert training_match in matches
        neg_matches = [example['match'] for example in neg_examples]
        for neg_match in neg_matches:
            assert neg_match in matches
        pos_matches = [training_match]
        if 'pos_examples' in case:
            pos_examples = case['pos_examples']
            for pos_example in pos_examples:
                pos_match = pos_example['match']
                pos_matches.append(pos_match)
        for pos_match in pos_matches:
            assert pos_match in matches
        # Find corresponding RolePatternMatches so we can access match_tokens
        pos_role_pattern_matches = [match for match in matches if match in pos_matches]
        neg_role_pattern_matches = [match for match in matches if match in neg_matches]
        refined_role_pattern_variants = role_pattern_builder.refine(
            pattern,
            pos_role_pattern_matches,
            neg_role_pattern_matches,
            feature_dicts=feature_dicts,
        )
        for role_pattern_variant in refined_role_pattern_variants:
            matches = [role_pattern_variant.match(d) for d in docs]
            matches = util.flatten_list(matches)
            for pos_match in pos_matches:
                assert pos_match in matches
            for neg_match in neg_matches:
                assert neg_match not in matches
            break  # Take only the first
        vis_outpath = 'examples/refined_pattern_vis/pattern_{0}_original.png'.format(
            case_i
        )
        pattern.write_vis(vis_outpath)
        vis_outpath = 'examples/refined_pattern_vis/pattern_{0}_refined.png'.format(
            case_i
        )
        role_pattern_variant.write_vis(vis_outpath)


def test_validate_features():
    match_examples = [
        {'slot1': idxs_to_tokens(doc1, [0, 1, 3])}  # [We, introduce, methods]
    ]
    feature_dict = {'DEP': 'dep_', 'TAG': 'tag_'}
    role_pattern_builder = RolePatternBuilder(feature_dict)
    features = ['DEP', 'TAG', 'LOWER']
    for match_example in match_examples:
        with pytest.raises(FeaturesNotInFeatureDictError):
            role_pattern_builder.build(match_example, features=features)


def test_visualise_pattern():
    for i, doc in enumerate(docs):
        png = visualise_spacy_tree.create_png(doc)
        filepath = 'examples/sentence_vis/sentence_{}.png'.format(i)
        with open(filepath, 'wb') as f:
            f.write(png)
    feature_dict = {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'}
    for test_i, case in enumerate(cases):
        match_example = case['training_example']['match']
        role_pattern_builder = RolePatternBuilder(feature_dict)
        for features_i, features in enumerate(feature_combs):
            role_pattern = role_pattern_builder.build(match_example, features=features)
            filepath = 'examples/spacy_dep_patterns/pattern_{}_{}.json'.format(
                test_i, features_i
            )
            with open(filepath, 'w') as f:
                json.dump(role_pattern.spacy_dep_pattern, f, indent=2)
            outpath = 'examples/pattern_vis/pattern_{0}_{1}.png'.format(
                test_i, features_i
            )
            role_pattern.write_vis(outpath, legend=True)


def test_visualise_pattern_legend():
    feature_dict = {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'}
    role_pattern_builder = RolePatternBuilder(feature_dict)
    case = cases[1]
    match_example = case['training_example']['match']
    role_pattern = role_pattern_builder.build(match_example)
    pydot, legend = role_pattern.to_pydot(legend=True)
    png = legend.create_png()
    filename = 'examples/pattern_vis/pattern_1_0_legend.png'
    with open(filename, 'wb') as f:
        f.write(png)


def test_visualise_pattern_match():
    feature_dict = {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'}
    for test_i, case in enumerate(cases):
        doc = case['training_example']['doc']
        match_example = case['training_example']['match']
        role_pattern_builder = RolePatternBuilder(feature_dict)
        for features_i, features in enumerate(feature_combs):
            role_pattern = role_pattern_builder.build(match_example, features=features)
            matches = role_pattern.match(doc)
            for match in matches:
                graph, legend = match.to_pydot(legend=True)
                png = graph.create_png()
                filename = 'examples/match_vis/match_{0}_{1}.png'.format(
                    test_i, features_i
                )
                with open(filename, 'wb') as f:
                    f.write(png)
    png = legend.create_png()
    filename = 'examples/match_vis/match_{0}_{1}_legend.png'.format(test_i, features_i)
    with open(filename, 'wb') as f:
        f.write(png)
