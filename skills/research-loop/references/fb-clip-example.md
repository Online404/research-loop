# FB-CLIP: an inspected placement map

This example illustrates locating real code boundaries before selecting donor modules. It is not a reproduction or an experimentally selected architecture. Inspection covered relevant method/protocol passages and source entry points; full-paper reading, tensor tracing and experimental validation remain to be done.

- Paper: [FB-CLIP, arXiv:2603.19608v1](https://arxiv.org/abs/2603.19608v1).
- Official code revision inspected on 2026-09-21: [`c097e7c39479e27651c0d94257053072f18d3549`](https://github.com/Xi-Mu-Yu/FB-CLIP/tree/c097e7c39479e27651c0d94257053072f18d3549).

## Existing boundaries to inspect for transfer

| Existing baseline component | Code boundary | When reading a donor paper, investigate |
|---|---|---|
| MSTFF text fusion | [`encode_text_learn`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L460) | Whether its token aggregation can replace the existing fusion while preserving normal/abnormal prototype semantics |
| MVFBE foreground/background enhancement | [`generate_fg_softmask`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L758), [`FG_BG_Enhancement`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L916) | Whether a spatial or token-selection operation can replace mask/refinement logic with compatible token order |
| Background suppression | [`extract_background_features`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L597), [`encode_all_image`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L940) | Whether the donor changes background prototype estimation or suppression, rather than duplicating the current operation |
| SCR objective | [`compute_semantic_consistency_loss`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L517) | Whether its alignment or regularization objective offers a compatible replacement or complementary constraint |

These are existing modules and prospective questions, not four new contributions. A candidate still needs an actual donor source, an interface contract and an experiment.

## Execution facts that affect candidate design

[`FB_encode`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/FBCLIP_lib/FBCLIP.py#L1001) returns classification output, an anomaly map and consistency loss. Inspect its caller in [`train_on_source_domain`](https://github.com/Xi-Mu-Yu/FB-CLIP/blob/c097e7c39479e27651c0d94257053072f18d3549/cross_domain_test.py#L219) when registering new trainable parameters and losses. Confirm checkpoint saving/loading and gradients on the actual forward path.

The baseline uses labeled source-domain training; preserve the source/target distinction in its zero-shot protocol. Verify the exact data usage in [paper §4.1](https://arxiv.org/html/2603.19608v1#S4.SS1) before choosing development data or a donor requiring supervision.

Two implementation details show why names alone are insufficient: the inspected text fusion uses fixed coefficients despite a declared fusion-weight parameter, and the enhancement's previous-token input is from the previous feature layer. Confirm active calculations instead of inferring learning or video inputs from variable names.

## First useful output

Fill `baseline.md` from these sources and a local forward trace. Then read one candidate paper and produce a transfer card naming its exact operation and one of the verified target boundaries. The next deliverable is that candidate's minimal implementation and controlled comparison, within the configured resources. No gain or completed 2–3-module model is claimed by this example.
