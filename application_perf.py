import pytest
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

class TestLatency:
    BASE_URL = 'http://servesentiment-env.eba-wzth6yic.us-east-1.elasticbeanstalk.com/'
    TEST_CASES = [
        ("honesty is the best policy.", 'real'),
        ("real news", 'real'),
        ("The moon is made of cheese.", 'fake'),
        ("Aliens have invaded Earth!", 'fake'),
    ]

    def test_latency(self):

        latencies = {expected: [] for _, expected in self.TEST_CASES}

        for text, expected in self.TEST_CASES:
            for _ in range(100):
                start_time = time.time()
                response = requests.post(self.BASE_URL, data={'text': text})
                end_time = time.time()


                latencies[expected].append(end_time - start_time)

            df = pd.DataFrame(latencies[expected], columns=['Latency'])
            df.to_csv(f'latency_results_{expected}.csv', index=False)


            average_latency = sum(latencies[expected]) / len(latencies[expected])
            print(f'Average Latency for "{expected}" test case: {average_latency:.4f} seconds')

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle('Latency Boxplots for Each Test Case')


        axs = axs.flatten()

 
        for ax, (text, expected) in zip(axs, self.TEST_CASES):
            ax.boxplot(latencies[expected])
            ax.set_title(expected.capitalize())
            ax.set_ylabel('Latency (seconds)')
            ax.set_xticks([1])
            ax.set_xticklabels([''])

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('latency_boxplot.png')
        plt.close()

if __name__ == "__main__":
    pytest.main()
