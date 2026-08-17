# Model Benchmark Report

## Model

Random Forest Classifier

- Number of estimators: 200
- Random state: 42

## Dataset

The model was trained using train.csv and evaluated using test.csv.

The label column was used as the target variable.

## Evaluation Results

| Metric | Result |
|---|---:|
| Accuracy | 99.72% |
| Average Inference Time | 47.1888 ms |
| Peak Memory Usage | 401.29 KB |
| Model Size | 8239.62 KB |
| Throughput | 21.19 predictions/sec |

## Accuracy

The Random Forest model achieved an accuracy of *99.72%* on the test dataset.

Accuracy was calculated by comparing the predicted labels with the actual labels in the test dataset.

## Inference Performance

The average inference time was *47.1888 ms per prediction*.

The measured throughput was *21.19 predictions per second*.

## Memory Usage

The peak memory usage during inference was *401.29 KB*.

## Model Size

The saved Random Forest model occupied approximately *8239.62 KB*.

## Conclusion

The benchmark demonstrates that the trained Random Forest model provides high classification accuracy while maintaining measurable inference performance and memory usage.

The model achieved *99.72% test accuracy* with an average inference time of *47.1888 ms* per prediction.