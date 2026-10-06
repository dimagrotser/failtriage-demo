# failtriage-demo

A tiny shop app with tests, set up so you can watch [failtriage](https://github.com/dimagrotser/ai-test-failure-triage) comment on a pull request. Branches that each break the app in a known way are ready, so you only open a pull request.

## Try it

1. Make your own copy: click "Use this template" on GitHub, or run

   ```
   gh repo create my-failtriage-demo --template dimagrotser/failtriage-demo --public --clone
   ```

2. Optional: add your `ANTHROPIC_API_KEY` under Settings, Secrets and variables, Actions. Without it the report comes from fixed rules alone, which is enough to see how the grouping works. With a key, an LLM classifies what the rules cannot.
3. In the copy, run `scripts/demo.sh all-at-once`. It puts one of the prepared breakages on a new branch, pushes it and opens a pull request. It needs `git` and a logged-in `gh`. A workflow cannot open the pull request for you, because pull requests opened with the built-in token do not start other workflows.
4. Wait about a minute for the `tests` job and read the comment failtriage leaves on the pull request. The full report is in the job summary too.

If you do not want to run the script, the same steps by hand are `git checkout -b demo/x`, `git apply demos/all-at-once.patch`, commit, push and open the pull request.

One run with a key sends at most a few groups to the model and costs a few cents.

## The breakages

| Name | What it breaks | Rules only | With a key |
|---|---|---|---|
| `product-bug` | `shop/cart.py` divides by the number of items, so an empty cart crashes | `product_bug`, low | `product_bug`, high |
| `test-bug` | a test expects 1300 where the code correctly returns 1350 | `unknown`, low | `test_bug`, high |
| `service-down` | the workflow no longer starts the rates stub, so the connection is refused | `environment`, medium | `environment`, medium |
| `all-at-once` | all three at once | 3 groups | 3 groups |

The rules only see where a test failed, so they stay at low confidence for an exception in source code and give up on a plain assertion mismatch. The model also reads the pull request diff, which is how it knows the 1300 in `test-bug` was typed in by the change.

The model is not deterministic, so its wording and its call on `test-bug` can differ between runs. The rules are deterministic.

This repository keeps one open pull request per breakage, so you can read the four comments without running anything.

## What the report says on a fresh copy

The comment can start with `History: none`. failtriage compares a failing test with earlier runs on `main` to spot flaky ones, and a new copy has no earlier runs yet. After a few pushes to `main` the line goes away.

## Run the tests locally

```
uv sync
uv run python -m shop.stub &
uv run pytest
```

The stub stands in for a rates service on port 8099. Stop it with `kill %1`.

## Limitations

The breakages are patches and not branches because GitHub gives every branch of a template copy its own history, so a pull request from one of them into `main` is refused.

There is no flaky branch. The usual way to show a flaky test is a plugin such as `pytest-rerunfailures`, but it writes the failed first attempt into the JUnit XML as a passed test, so failtriage cannot see the retry. I left that case out instead of faking it.

The workflow asks for `pull-requests: write`, `actions: read` and `contents: read`, nothing more. On pull requests from forks GitHub hands out a read-only token and no secrets, so there the report goes to the job summary and only the rules run.
