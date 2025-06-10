# File Descriptions

These files show exchanges between two nearly identical installations of the pi-llm models. One install is on an amd64 desktop computer and one is on a Raspberry Pi 4B device (aarch64). For the span of the test the two computers are not given human input. They just interact with each other. In the table, if a 'collision' is mentioned, that indicates that the two models were talking at the same time.

| file | description | date |
|---|---|---|
| llm.05a.txt | 15 minutes, 13 responses, 0.95 temperature, 3 collisions, use cloud speech recognition, no collision checking, name Bob | 2024-07-20 |
| llm.05b.txt | 15 minutes, 13 responses, 0.95 temperature, 3 collisions, use cloud speech recognition, no collision checking, name Jane | 2024-07-20 |
| llm.gpt-3.5-turbo_a.txt | 15 minutes, name Jane | 2024-07-27 |
| llm.gpt-3.5-turbo_b.txt | 15 minutes, name Bob | 2024-07-27 |
| llm.gpt-4o-mini_a.txt | 15 minutes, name Jane (epoch 00) | 2024-07-30 |
| llm.gpt-4o-mini_b.txt | 15 minutes, name Bob (epoch 00) | 2024-07-30 |
| llm.gpt-4o-mini-epoch01.txt | 15 minutes, name Jane | 2024-08-29 |
| llm.gpt-4o-mini-epoch02.txt | 15 minutes, name Jane | 2024-08-29 |

## 2025-03-29 

Note: exchanges for this date range require `--truncate` option.

| file | description | date |
|---|---|---|
| llm.gpt-3.5-turbo_2025_03_29.txt | less than 10 minutes, truncate option used, 9 exchanges, no interruptions or collisions | 2025-03-29 |

## 2025-04-04 

Note: exchanges are tested without the `--truncate` option. The interactions in this file start off as 'Hello' type statements, but quickly moves to 'Goodbye' type statements. After that the models repeat the 'Goodbye' sentiment until the end of the exchange.

| file | description | date |
|---|---|---|
| llm.gpt-3.5-turbo_2025_04_04.txt | 5 minutes, 15 responses, female, name Jane, 0 collisions, use cloud speech stt module. | 2025-04-04 |

Of special note, there are no interruptions or collisions in this interaction.

## 2025-04-23 

Note: exchanges are tested with the `--truncate` option. The interactions in this file start off as 'Hello' type statements, but quickly moves to 'Thank you' and 'You're Welcome' type statements. After that the models repeat the 'Thank you' sentiment until the end of the exchange.

| file | description | date |
|---|---|---|
| llm.gpt-4o_2025_04_23.txt | 5 minutes, 17 responses, female, name Jane, 0 collisions, use cloud speech stt module. | 2025-04-23 |

Of special note, there are no interruptions or collisions in this interaction because of the `--truncate` option.
