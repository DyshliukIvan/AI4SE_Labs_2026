# Report 5

The pipeline retrieves five chunks for each task, sends them with the task to the model and writes the returned method body. I ran all ten tasks from missing_code.json using gpt-4o-mini, then gpt-5-mini with test feedback.

| Attempt | Failures | Errors |
| --- | ---: | ---: |
| Original code | 35 | 17 |
| gpt-4o-mini | 2 | 10 |
| gpt-4o-mini repair | 2 | 9 |
| gpt-5-mini | 0 | 7 |
| Final pricing repair | 0 | 0 |

All 481 tests passed after the final repair. The tests were unchanged. InventoryLedger.__contains__ follows the supplied test, which expects a previously stocked SKU to remain present at zero stock, unlike the task description.
