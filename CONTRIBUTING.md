# Contributing to RAG Debug Lab

Help make one small retrieval debugging exercise easier to understand and run. Reports of confusion are as useful as code changes.

## Try the exercise first

Follow the [README quick start](README.md#quick-start). For an attempt report, use [Tried the lab](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/issues/new?template=tried-the-lab.yml). Say whether you read the material, ran the starter, wrote a fix or ran the reference. A 6/6 reference result does not mean you solved the exercise yourself.

**The starter is intentionally broken.** Do not submit a pull request replacing `chunking.py` with the solution. That removes the exercise for the next learner. Keep your personal repair in your own copy.

## Useful contributions

- Explain a setup step that was unclear, including the operating system and Python version.
- Report a broken link, unexpected exception or discrepancy between code and documentation.
- Suggest a clearer hint without revealing the entire repair immediately.
- Review heading scope, paragraph preservation or existing checks against the stated fixture format.
- Propose a new failure scenario in an issue before adding dependencies or expanding the lab.

Use the [bug-report form](https://github.com/Dharani-Eswaramurthi/rag-debug-lab/issues/new?template=bug-report.yml) for unexpected defects. Existing baseline failures and unsupported questions described in the README are known limitations, not proof of a new defect. Improvements to those limitations need an agreed exercise design.

## Make a change

1. Create your own branch or fork, then keep the change focused.
2. Use Python 3.10+; the exercise and tests require only its standard library.
3. Run `python -m unittest discover -s tests -v` from the repository root. All 17 tests should pass.
4. Check `python lab.py --baseline --check` still reports 2/6 with exit code 1, and `python lab.py --reference --check` reports 6/6 with exit code 0.
5. Explain the problem, change, and checks in your pull request. For documentation changes, verify commands and relative links.

Preserve the fictional fixtures, avoid hardcoded workspace names in general parsing logic, and distinguish the automated harness from learner outcomes. Do not introduce network calls, telemetry, signup requirements or paid dependencies into this offline exercise.

If AI helped with a contribution, explain its role and verify the submitted code, prose and references yourself. Do not claim learner testing or independent review unless it actually happened.

## Respect and privacy

Be constructive and specific. Critique the work without personal attacks. Public issues and pull requests must not contain credentials, private documents, customer information or personal contact details. For private feedback, use the email route in the README. Do not publish another person's feedback or identity without permission.

Contributions are intended to be distributed under the repository's existing [MIT license](LICENSE). Only submit material you have the right to share.
