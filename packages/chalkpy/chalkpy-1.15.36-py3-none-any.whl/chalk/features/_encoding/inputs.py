from collections.abc import Mapping as MappingABC
from typing import Any, Dict, List, Mapping, Optional, Tuple

from chalk.features import Feature, FeatureNotFoundException, Features, ensure_feature


def recursive_encode(inputs: Mapping, feature_cls: Optional[Features]) -> Tuple[Dict[str, Any], List]:
    all_warnings = []
    encoded_inputs = {}
    for k, v in inputs.items():
        fqn = k
        if feature_cls is not None:
            fqn = f"{feature_cls.__chalk_namespace__}.{k}"
        try:
            feature = ensure_feature(fqn)
        except FeatureNotFoundException:
            all_warnings.append(f"Input {fqn} not recognized. JSON encoding {fqn} and requesting anyways")
            encoded_inputs[k] = v
            continue

        encoded_key = feature.fqn if feature_cls is None else k
        if feature.is_has_many:
            _validate_has_many_value(v, feature)

            has_many_result = []
            for item in v:
                result, inner_warnings = recursive_encode(item, feature.joined_class)
                all_warnings = all_warnings + inner_warnings
                has_many_result.append(result)

            encoded_inputs[encoded_key] = has_many_result
        else:
            encoded_inputs[encoded_key] = feature.converter.from_rich_to_json(
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
