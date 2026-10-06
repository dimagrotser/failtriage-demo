# failtriage-demo

A tiny shop app with tests, set up so you can watch [failtriage](https://github.com/dimagrotser/ai-test-failure-triage) comment on a pull request. Branches that each break the app in a known way are ready, so you only open a pull request.

## Try it

1. Make a copy of this repository, with all branches. In the browser, click "Use this template" and tick "Include all branches". From the terminal:

   ```
   gh repo create my-failtriage-demo --template dimagrotser/failtriage-demo --include-all-branches --public
   ```

2. Optional: add your `ANTHROPIC_API_KEY` under Settings, Secrets and variables, Actions. Without it the report comes from fixed rules alone, which is enough to see how the grouping works. With a key, an LLM classifies what the rules cannot.
3. Open a pull request from one of the `demo/*` branches into `main`. A workflow cannot do this for you, because pull requests opened with the built-in token do not start other workflows.
4. Wait about a minute for the `tests` job and read the comment failtriage leaves on the pull request. The full report is in the job summary too.

One run with a key sends at most a few groups to the model and costs a few cents.

## The branches

| Branch | What it breaks | What failtriage should say |
|---|---|---|
| `demo/product-bug` | `shop/cart.py` divides by the number of items, so an empty cart crashes | `product_bug`, low confidence. The failing frame is in source code, but the rules never go above low for that |
| `demo/test-bug` | a test expects 1300 where the code correctly returns 1350 | `unknown` from the rules. With a key the model sees the diff and may call it `test_bug` |
| `demo/service-down` | the workflow no longer starts the rates stub, so the connection is refused | `environment`, medium confidence |
| `demo/all-at-once` | all three at once | 3 groups in one comment |

The model is not deterministic, so its wording and its call on `demo/test-bug` can differ between runs. The rules are deterministic.

## What the report says on a fresh copy

The comment starts with `History: none`. failtriage compares a failing test with earlier runs on `main` to spot flaky ones, and a new copy has no earlier runs yet. After a few pushes to `main` the line goes away.

## Run the tests locally

```
uv sync
uv run python -m shop.stub &
uv run pytest
```

The stub stands in for a rates service on port 8099. Stop it with `kill %1`.

## Limitations

There is no flaky branch. The usual way to show a flaky test is a plugin such as `pytest-rerunfailures`, but it writes the failed first attempt into the JUnit XML as a passed test, so failtriage cannot see the retry. I left that case out instead of faking it.

The workflow asks for `pull-requests: write`, `actions: read` and `contents: read`, nothing more. On pull requests from forks GitHub hands out a read-only token and no secrets, so there the report goes to the job summary and only the rules run.
