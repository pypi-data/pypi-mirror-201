from collections.abc import Mapping as MappingABC
from typing import Any, Dict, List, Mapping, Optional, Tuple

from chalk.features import Feature, FeatureNotFoundException, Features, ensure_feature


def recursive_encode(inputs: Mapping) -> Tuple[Dict[str, Any], List]:
    all_warnings = []
    encoded_inputs = {}
    for fqn, v in inputs.items():
        try:
            feature = ensure_feature(fqn)
        except FeatureNotFoundException:
            all_warnings.append(f"Input {fqn} not recognized. JSON encoding {fqn} and requesting anyways")
            encoded_inputs[fqn] = v
            continue

        if feature.is_has_many:
            _validate_has_many_value(v, feature)

            has_many_result = []
            for item in v:
                result, inner_warnings = recursive_encode(item)
                all_warnings = all_warnings + inner_warnings
                has_many_result.append(result)

            encoded_inputs[feature.root_fqn] = has_many_result
        else:
            encoded_inputs[feature.root_fqn] = feature.converter.from_rich_to_json(
                v,
                missing_value_strategy="error",
            )

    return encoded_inputs, all_warnings


def _validate_has_many_value(v: Any, feature: Feature):
    if not isinstance(v, list):
        raise TypeError(f"has-many feature '{feature.fqn}' must be a list, but got {type(v).__name__}")

    for item in v:
        if not isinstance(item, MappingABC):
            raise TypeError(
                f"has-many feature '{feature.fqn}' must be a list of Mapping, but got a list of {type(item).__name__}"
            )
