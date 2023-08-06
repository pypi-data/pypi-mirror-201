from __future__ import annotations

from typeguard import typechecked
from Levenshtein import ratio, setratio
from typing import Optional, Any

import erdiagram

scores = dict()
ratio_threshold = 0


@typechecked
def grade_submission(
    solution: erdiagram.ER,
    submission: erdiagram.ER,
    *,
    score_missing_node: float = 1,
    score_missing_entity_property: float = 0.5,
    score_missing_attribute_property: float = 0.25,
    score_missing_composed_attribute_property: float = 0.125,
    score_missing_relation_property: float = 0.5,
    score_missing_is_a_property: float = 0.25,
    label_ratio_threshold: float = 0.8,
) -> tuple[float, str]:
    """
    Grades a submission given a solution. Returns the score.

    Parameters
    ----------
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram.
    score_missing_node : float, optional
        The score to be deducted for each completely missing node, by default 1
    score_missing_entity_property : float, optional
        The score to be deducted for each missing entity property, by default 0.5
    score_missing_attribute_property : float, optional
        The score to be deducted for each missing attribute property, by default 0.25
    score_missing_composed_attribute_property : float, optional
        The score to be deducted for each missing composed attribute property, by default 0.125
    score_missing_relation_property : float, optional
        The score to be deducted for each missing relation property, by default 0.5
    score_missing_is_a_property : float, optional
        The score to be deducted for each missing is-a relation property, by default 0.25
    label_ratio_threshold : float, optional
        The minimum label ratio for two entities to be considered equal, by default 0.8

    Returns
    -------
    tuple[float, str]
        The score and the grading log.
    """
    global scores
    scores = {
        "missing_node": score_missing_node,
        "missing_entity_property": score_missing_entity_property,
        "missing_attribute_property": score_missing_attribute_property,
        "missing_composed_attribute_property": score_missing_composed_attribute_property,
        "missing_relation_property": score_missing_relation_property,
        "missing_is_a_property": score_missing_is_a_property,
    }
    global ratio_threshold
    ratio_threshold = label_ratio_threshold

    score = 0
    log = ""

    # Grade entities
    sub_score, sub_log = _grade_entities(solution, submission)
    score += sub_score
    log += sub_log

    # Grade relations
    sub_score, sub_log = _grade_relations(solution, submission)
    score += sub_score
    log += sub_log

    # Grade is-a relations
    sub_score, sub_log = _grade_is_as(solution, submission)
    score += sub_score
    log += sub_log

    # Grade attributes
    sub_score, sub_log = _grade_attributes(solution, submission)
    score += sub_score
    log += sub_log

    return score, log


def _grade_entity_pair(
    entity_pair: tuple[dict[str, Any], dict[str, Any]],
    solution: erdiagram.ER,
    submission: erdiagram.ER,
) -> Optional[tuple[float, str]]:
    """
    Grades a pair of entities.

    Parameters
    ----------
    entity_pair : tuple[dict[str, Any], dict[str, Any]]
        The pair of entities to grade. (solution_entity, submission_entity)
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram

    Returns
    -------
    Optional[tuple[float, str]]
        The score and the grading log. None if the entities are not comparable.
    """
    score = 0
    log = ""

    solution_entity, submission_entity = entity_pair
    original_solution_label, original_submission_label = (
        solution_entity["label"],
        submission_entity["label"],
    )
    solution_label, submission_label = sanitize(original_solution_label), sanitize(
        original_submission_label
    )
    label_ratio = ratio(solution_label, submission_label)

    if label_ratio < ratio_threshold:
        return None

    log += f"\t✓ Entity '{original_solution_label}' was found. (Matched against '{original_submission_label}' with a label ratio of {label_ratio:.2f}) \n"

    # Check properties `is_multiple` and `is_weak`
    if solution_entity["is_multiple"] != submission_entity["is_multiple"]:
        score += scores["missing_entity_property"]
        log += f"\t✗ Entity '{original_solution_label}' should be {'multiple' if solution_entity['is_multiple'] else 'not multiple'}. ({scores['missing_entity_property']})\n"
    else:
        log += f"\t✓ Entity '{original_solution_label}' is {'multiple' if solution_entity['is_multiple'] else 'not multiple'}.\n"

    if solution_entity["is_weak"] != submission_entity["is_weak"]:
        score += scores["missing_entity_property"]
        log += f"\t✗ Entity '{original_solution_label}' should be {'weak' if solution_entity['is_weak'] else 'not weak'}. ({scores['missing_entity_property']})\n"
    else:
        log += f"\t✓ Entity '{original_solution_label}' is {'weak' if solution_entity['is_weak'] else 'not weak'}.\n"

    return score, log


@typechecked
def _grade_entities(
    solution: erdiagram.ER, submission: erdiagram.ER
) -> tuple[float, str]:
    """
    Grades the entities of a submission given a solution. Returns the score.

    Parameters
    ----------
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram.

    Returns
    -------
    tuple[float, str]
        The score and the grading log.
    """
    score = 0
    log = ""

    # determine a grade for each entity in the submission
    for solution_entity in solution.get_entities():
        solution_label = solution_entity["label"]
        log += f"\n» Searching for entity {solution_label} in submission.\n"

        graded_entity_pairs = [
            _grade_entity_pair(
                (solution_entity, submission_entity), solution, submission
            )
            for submission_entity in submission.get_entities()
        ]
        graded_entity_pairs = [pair for pair in graded_entity_pairs if pair is not None]
        if len(graded_entity_pairs) > 0:  # entity found
            sub_score, sub_log = min(graded_entity_pairs, key=lambda pair: pair[0])
            score += sub_score
            log += sub_log
            continue

        # entity not found
        log += f"\t✗ Entity '{solution_label}' not found in submission. ({scores['missing_node']})\n"
        score += scores["missing_node"]

    return score, log


@typechecked
def _grade_relation_pair(
    relation_pair: tuple[dict[str, Any], dict[str, Any]],
    solution: erdiagram.ER,
    submission: erdiagram.ER,
) -> Optional[tuple[float, str]]:
    """
    Grades a pair of relations.

    Parameters
    ----------
    relation_pair : tuple[dict[str, Any], dict[str, Any]]
        The pair of relations to grade. (solution_relation, submission_relation)
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram

    Returns
    -------
    Optional[tuple[float, str]]
        The score and the grading log. None if the relations are not comparable.
    """
    score = 0
    log = ""

    solution_relation, submission_relation = relation_pair
    original_solution_label, original_submission_label = (
        solution_relation["label"],
        submission_relation["label"],
    )
    solution_label, submission_label = sanitize(original_solution_label), sanitize(
        original_submission_label
    )
    label_ratio = ratio(solution_label, submission_label)

    log += f"\t✓ Relation '{original_solution_label} found. (Matched against '{original_submission_label}' with a label ratio of {label_ratio:.2f}) \n"

    transform_dict_to_list = lambda x: [{"label": k, **v} for k, v in x.items()]
    from_entities_solution = transform_dict_to_list(solution_relation["from_entities"])
    from_entities_submission = transform_dict_to_list(
        submission_relation["from_entities"]
    )
    to_entities_solution = transform_dict_to_list(solution_relation["to_entities"])
    to_entities_submission = transform_dict_to_list(submission_relation["to_entities"])

    # match from entities based on highest label ratio as tuples (solution, submission)
    from_entity_pairs = []
    for solution_from_entity in from_entities_solution:
        from_entity_pairs.append(
            (
                solution_from_entity,
                max(
                    from_entities_submission,
                    key=lambda submission_from_entity: ratio(
                        sanitize(solution_from_entity["label"]),
                        sanitize(submission_from_entity["label"]),
                    ),
                ),
            )
        )
    to_entity_pairs = []
    for solution_to_entity in to_entities_solution:
        to_entity_pairs.append(
            (
                solution_to_entity,
                max(
                    to_entities_submission,
                    key=lambda submission_to_entity: ratio(
                        sanitize(solution_to_entity["label"]),
                        sanitize(submission_to_entity["label"]),
                    ),
                ),
            )
        )

    for solution_from_entity, submission_from_entity in from_entity_pairs:
        original_solution_from_entity_label = solution_from_entity["label"]
        original_submission_from_entity_label = submission_from_entity["label"]
        solution_from_entity_label = sanitize(original_solution_from_entity_label)
        submission_from_entity_label = sanitize(original_submission_from_entity_label)
        label_ratio = ratio(solution_from_entity_label, submission_from_entity_label)
        if label_ratio < ratio_threshold:
            score += scores["missing_relation_property"] * 3
            log += f"\t✗ Relation '{original_solution_label}' should have a from entity '{original_solution_from_entity_label}'. ({scores['missing_relation_property'] * 3})\n"
            continue

        log += f"\t✓ Relation '{original_solution_label}' has a from entity '{original_solution_from_entity_label}' comparable to '{original_submission_from_entity_label}' with a label ratio of {label_ratio:.2f}.\n"

        # check for the same cardinality
        solution_from_entity_cardinality = solution_from_entity["cardinality"]
        submission_from_entity_cardinality = submission_from_entity["cardinality"]
        if str(solution_from_entity_cardinality).replace(" ", "") != str(
            submission_from_entity_cardinality
        ).replace(" ", ""):
            score += scores["missing_relation_property"]
            log += f"\t✗ Relation '{original_solution_label}' should have a from entity '{original_solution_from_entity_label}' with cardinality '{solution_from_entity_cardinality}', but has '{submission_from_entity_cardinality}'. ({scores['missing_relation_property']})\n"

        # check for the same is_weak
        solution_from_entity_is_weak = solution_from_entity["is_weak"]
        submission_from_entity_is_weak = submission_from_entity["is_weak"]
        if solution_from_entity_is_weak != submission_from_entity_is_weak:
            score += scores["missing_relation_property"]
            log += f"\t✗ Relation '{original_solution_label}' should have a from entity '{original_solution_from_entity_label}' {'weak' if solution_from_entity_is_weak else 'not weak'}, but is {'weak' if submission_from_entity_is_weak else 'not weak'}. ({scores['missing_relation_property']})\n"

    for solution_to_entity, submission_to_entity in to_entity_pairs:
        original_solution_to_entity_label = solution_to_entity["label"]
        original_submission_to_entity_label = submission_to_entity["label"]
        solution_to_entity_label = sanitize(original_solution_to_entity_label)
        submission_to_entity_label = sanitize(original_submission_to_entity_label)
        label_ratio = ratio(solution_to_entity_label, submission_to_entity_label)
        if label_ratio < ratio_threshold:
            score += scores["missing_relation_property"] * 3
            log += f"\t✗ Relation '{original_solution_label}' should have a to entity '{original_solution_to_entity_label}'. ({scores['missing_relation_property'] * 3})\n"
            continue

        log += f"\t✓ Relation '{original_solution_label}' has a to entity '{original_solution_to_entity_label}' comparable to '{original_submission_to_entity_label}' with a label ratio of {label_ratio:.2f}.\n"

        # check for the same cardinality
        solution_to_entity_cardinality = solution_to_entity["cardinality"]
        submission_to_entity_cardinality = submission_to_entity["cardinality"]
        if str(solution_to_entity_cardinality).replace(" ", "") != str(
            submission_to_entity_cardinality
        ).replace(" ", ""):
            score += scores["missing_relation_property"]
            log += f"\t✗ Relation '{original_solution_label}' should have a to entity '{original_solution_to_entity_label}' with cardinality '{solution_to_entity_cardinality}', but has '{submission_to_entity_cardinality}'. ({scores['missing_relation_property']})\n"

        # check for the same is_weak
        solution_to_entity_is_weak = solution_to_entity["is_weak"]
        submission_to_entity_is_weak = submission_to_entity["is_weak"]
        if solution_to_entity_is_weak != submission_to_entity_is_weak:
            score += scores["missing_relation_property"]
            log += f"\t✗ Relation '{original_solution_label}' should have a to entity '{original_solution_to_entity_label}' {'weak' if solution_to_entity_is_weak else 'not weak'}, but is {'weak' if submission_to_entity_is_weak else 'not weak'}. ({scores['missing_relation_property']})\n"

    return score, log


@typechecked
def _grade_relations(
    solution: erdiagram.ER, submission: erdiagram.ER
) -> tuple[float, str]:
    """
    Grades the relations of a submission given a solution. Returns the score.

    Parameters
    ----------
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram.

    Returns
    -------
    tuple[float, str]
        The score and the grading log.
    """
    score = 0
    log = ""

    for solution_relation in solution.get_relations():
        solution_label = solution_relation["label"]
        log += f"\n» Searching for relation {solution_label} in submission.\n"

        graded_relation_pairs = [
            _grade_relation_pair(
                (solution_relation, submission_relation), solution, submission
            )
            for submission_relation in submission.get_relations()
        ]
        graded_relation_pairs = [
            pair for pair in graded_relation_pairs if pair is not None
        ]
        if len(graded_relation_pairs) > 0:  # relation found
            sub_score, sub_log = min(graded_relation_pairs, key=lambda pair: pair[0])
            score += sub_score
            log += sub_log
            continue

        # Score missing node
        s = scores["missing_node"] * (
            len(solution_relation["from_entities"])
            * len(solution_relation["to_entities"])
        )
        score += s
        # relation not found
        log += f"\t✗ Relation '{solution_label}' not found in submission. ({s})\n"

    return score, log


@typechecked
def _grade_is_as(solution: erdiagram.ER, submission: erdiagram.ER) -> tuple[float, str]:
    """
    Grades the is-a relations of a submission given a solution. Returns the score.

    Parameters
    ----------
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram.

    Returns
    -------
    tuple[float, str]
        The score and the grading log.
    """
    score = 0
    log = ""
    for solution_is_a in solution.get_is_as():
        solution_super_label = solution.get_entity_by_id(
            solution_is_a["superclass_id"]
        )["label"]
        solution_sub_labels = [
            solution.get_entity_by_id(sub_id)["label"]
            for sub_id in solution_is_a["subclass_ids"]
        ]

        log += f"\n» Searching for is-a relation {solution_super_label} -> {solution_sub_labels} in submission.\n"

        submission_is_a = max(
            filter(
                lambda pair: pair[1] > ratio_threshold,
                [
                    (
                        possible_submission_is_a,
                        ratio(
                            sanitize(solution_super_label),
                            sanitize(
                                submission.get_entity_by_id(
                                    possible_submission_is_a["superclass_id"]
                                )["label"]
                            ),
                        ),
                    )
                    for possible_submission_is_a in submission.get_is_as()
                ],
            ),
            key=lambda pair: pair[1],
            default=None,
        )
        if submission_is_a is None:
            s = scores["missing_node"]
            score += s
            log += f"\t✗ Is-a relation {solution_super_label} -> {solution_sub_labels} not found in submission. ({s})\n"
            continue

        log += f"\t✓ Is-a relation {solution_super_label} -> {solution_sub_labels} found in submission. (Matched against {submission.get_entity_by_id(submission_is_a[0]['superclass_id'])['label']} -> {[submission.get_entity_by_id(sub_id)['label'] for sub_id in submission_is_a[0]['subclass_ids']]} with a ratio of {submission_is_a[1]:.2f})\n"

        # check if the subclasses are the same
        submission_super_label = submission.get_entity_by_id(
            submission_is_a[0]["superclass_id"]
        )["label"]
        submission_sub_labels = [
            submission.get_entity_by_id(sub_id)["label"]
            for sub_id in submission_is_a[0]["subclass_ids"]
        ]

        set_ratio = setratio(
            set([sanitize(label) for label in solution_sub_labels]),
            set([sanitize(label) for label in submission_sub_labels]),
        )

        if set_ratio < ratio_threshold:
            s = scores["missing_is_a_property"] * len(solution_sub_labels) * set_ratio
            score += s
            log += f"\t✗ The is-a relation {solution_super_label} -> {solution_sub_labels} is not comparable to {submission_super_label} -> {submission_sub_labels} with a set ratio of {set_ratio:.2f}. ({s})\n"

        # check if the custom text is the same
        solution_custom_text = solution_is_a["custom_text"]
        submission_custom_text = submission_is_a[0]["custom_text"]
        if (solution_custom_text is not None and submission_custom_text is None) or (
            solution_custom_text is None and submission_custom_text is not None
        ):
            log += f"\t✗ The is-a relation {solution_super_label} -> {solution_sub_labels} should{' not' if solution_custom_text is None else ''} have a custom text. ({scores['missing_is_a_property']})\n"
            score += scores["missing_is_a_property"]
        elif solution_custom_text is not None and submission_custom_text is not None:
            label_ratio = ratio(
                sanitize(solution_custom_text), sanitize(submission_custom_text)
            )
            if label_ratio < ratio_threshold:
                s = scores["missing_is_a_property"] * label_ratio
                score += s
                log += f"\t✗ The is-a relation {solution_super_label} -> {solution_sub_labels} has a custom text with a ratio of {label_ratio:.2f}. ({s})\n"

        # check if `is_total` and `is_disjunct` are the same
        if solution_is_a["is_total"] != submission_is_a[0]["is_total"]:
            log += f"\t✗ The is-a relation {solution_super_label} -> {solution_sub_labels} should{' not' if solution_is_a['is_total'] else ''} be total. ({scores['missing_is_a_property']})\n"
            score += scores["missing_is_a_property"]
        if solution_is_a["is_disjunct"] != submission_is_a[0]["is_disjunct"]:
            log += f"\t✗ The is-a relation {solution_super_label} -> {solution_sub_labels} should{' not' if solution_is_a['is_disjunct'] else ''} be disjunct. ({scores['missing_is_a_property']})\n"
            score += scores["missing_is_a_property"]

    return score, log


@typechecked
def _grade_attributes(
    solution: erdiagram.ER, submission: erdiagram.ER
) -> tuple[float, str]:
    """
    Grades the attributes of a submission given a solution. Returns the score.

    Parameters
    ----------
    solution : erdiagram.ER
        The solution diagram.
    submission : erdiagram.ER
        The submission diagram.

    Returns
    -------
    tuple[float, str]
        The score and the grading log.
    """
    score = 0
    log = ""
    for solution_attribute in solution.get_attributes():
        solution_attribute_label = solution_attribute["label"]
        solution_parent_label = solution.get_label_by_id(
            solution_attribute["parent_id"]
        )
        solution_parent_type = solution_attribute["parent_type"]

        log += f"\n» Searching for attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} in submission.\n"

        # Filter possible attributes by parent type and ratio threshold
        filtered_attributes = list(
            filter(
                lambda pair: pair[1] >= ratio_threshold,
                [
                    (
                        possible_submission_attribute,
                        ratio(
                            sanitize(solution_parent_label),
                            sanitize(
                                submission.get_label_by_id(
                                    possible_submission_attribute["parent_id"]
                                )
                            ),
                        ),
                    )
                    for possible_submission_attribute in submission.get_attributes()
                    if possible_submission_attribute["parent_type"]
                    == solution_parent_type
                ],
            )
        )

        # Find maximal ratio value
        max_ratio = max([pair[1] for pair in filtered_attributes], default=None)

        # Filter attributes with maximal ratio value
        maximal_attributes = [
            pair[0] for pair in filtered_attributes if pair[1] == max_ratio
        ]

        # Filter the attributes by label ratio above threshold, and get the one with maximal label ratio
        submission_attribute = max(
            list(
                filter(
                    lambda pair: pair[1] >= ratio_threshold,
                    [
                        (
                            possible_submission_attribute,
                            ratio(
                                sanitize(solution_attribute_label),
                                sanitize(possible_submission_attribute["label"]),
                            ),
                        )
                        for possible_submission_attribute in maximal_attributes
                    ],
                )
            ),
            key=lambda pair: pair[1],
            default=None,
        )

        if submission_attribute is None:
            s = scores["missing_attribute_property"]
            score += s
            log += f"\t✗ Attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} not found in submission.({s})\n"
            continue

        log += f"\t✓ Attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} found in submission. (Matched against submission attribute {submission_attribute[0]['label']} of {str(submission_attribute[0]['parent_type']).lower()} {submission.get_label_by_id(submission_attribute[0]['parent_id'])} with ratio {submission_attribute[1]:.2f})\n"

        # check if `is_pk`, `is_multiple`, and `is_weak` are the same
        if solution_attribute["is_pk"] != submission_attribute[0]["is_pk"]:
            log += f"\t✗ The attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} should{' not' if solution_attribute['is_pk'] else ''} be a primary key. ({scores['missing_attribute_property']})\n"
            score += scores["missing_attribute_property"]
        if solution_attribute["is_multiple"] != submission_attribute[0]["is_multiple"]:
            log += f"\t✗ The attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} should{' not' if solution_attribute['is_multiple'] else ''} be multiple. ({scores['missing_attribute_property']})\n"
            score += scores["missing_attribute_property"]
        if solution_attribute["is_weak"] != submission_attribute[0]["is_weak"]:
            log += f"\t✗ The attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} should{' not' if solution_attribute['is_weak'] else ''} be weak. ({scores['missing_attribute_property']})\n"
            score += scores["missing_attribute_property"]

        solution_composed_attribute_labels = [
            sanitize(solution.get_label_by_id(composed_attribute_id))
            for composed_attribute_id in solution_attribute["composed_of_attribute_ids"]
        ]
        submission_composed_attribute_labels = [
            sanitize(submission.get_label_by_id(composed_attribute_id))
            for composed_attribute_id in submission_attribute[0][
                "composed_of_attribute_ids"
            ]
        ]
        set_ratio = setratio(
            solution_composed_attribute_labels, submission_composed_attribute_labels
        )
        if set_ratio < ratio_threshold:
            s = (
                scores["missing_attribute_property"]
                * len(solution_attribute["composed_of_attribute_ids"])
                * set_ratio
            )
            score += s
            log += f"\t✗ The attribute {solution_attribute_label} of {str(solution_parent_type).lower()} {solution_parent_label} has a different composition. ({s})\n"

    return score, log


@typechecked
def sanitize(s: str) -> str:
    """
    Sanitizes a string for comparison.

    Parameters
    ----------
    s : str
        The string to sanitize.

    Returns
    -------
    str
        The sanitized string.
    """
    return s.lower().strip().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
