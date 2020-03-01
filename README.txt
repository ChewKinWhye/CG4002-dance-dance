The aim of this project is to be able to detect the dance moves by using the data input from
gyroscopes and accelerometers attached to both of the user's hands.

Steps:
Collecting data
Loading data
Pre-processing data
- Split data into fixed steps, normalization, one-hot encoding, feature extraction, feature selection,

Training model
- Convolution Neural Networks, Feed Forward Neural Networks
Testing model
- K-fold cross validation, classification accuracy, confusion matrix
Tuning hyper-parameters
- Window size, overlap size, batch size, layers, nodes, features to use


Features to extract
t body acceleration
0 1 2 3 25 28 29 32 33 36 37 38 39

t gravity acc 40 41 42 43 44 45 55 62 63 64 65 69 73 77 78 79

t body acc jerk
80 106 107 108 111 112 115 116 117 118 119

t body gyro
120 121 122 142 143 144 145 148 149 151 152 153 156 157 158 159

t body gyro jerk
160 161 162 186 187 188 190 192 195 196 197 198 199

t body acc mag
209 211

t body acc jerk mag
235 238

t body gyro mag
247 248 250

t body gyro jerk mag
261 262 263 264

f body acc
277 278 279 290 291 292 293 294 295 296 298 300 323

f body acc jerk
356 357 358 369 370 371 375 377 379 388 402 416

f body gyro
435 436 437 448 449 450 451 452 453 454 456 458 481 494

f body acc mag
506 511 512 513

f body acc jerk mag
519 524 525 526

f body gyro mag
532 537 539

f body gyro jerk mag
550 551 552 555 556 557