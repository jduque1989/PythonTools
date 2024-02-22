import subprocess
import re
import matplotlib.pyplot as plt
import sys
import numpy as np


def run_speedtest():
    result = subprocess.run(["speedtest"], capture_output=True, text=True)
    return result.stdout


def extract_data(output):
    patterns = {
        'download': r'Download:.*?(\d+\.\d+) Mbps',
        'upload': r'Upload:.*?(\d+\.\d+) Mbps',
        'latency': r'Latency:.*?(\d+\.\d+) ms',
        'jitter': r'jitter: (\d+\.\d+)ms',
        'low': r'low: (\d+\.\d+)ms',
        'high': r'high: (\d+\.\d+)ms'
    }
    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            results[key] = float(match.group(1))
        else:
            print(f"Error: Unable to find {key} in the output.")
            results[key] = 0.0
    return results


def plot_speeds(download_speeds, upload_speeds):
    # Creating figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Linear regression for download speeds
    x = np.arange(len(download_speeds))
    slope, intercept = np.polyfit(x, download_speeds, 1)
    ax1.plot(download_speeds, label='Download Speeds (Mbps)', color='blue')
    ax1.plot(x, slope * x + intercept, label='Linear Regression', linestyle='--', color='red')

    # Linear regression for upload speeds
    slope, intercept = np.polyfit(x, upload_speeds, 1)
    ax2.plot(upload_speeds, label='Upload Speeds (Mbps)', color='green')
    ax2.plot(x, slope * x + intercept, label='Linear Regression', linestyle='--', color='orange')

    # Setting labels and titles
    ax1.set_xlabel('Test Number')
    ax1.set_ylabel('Download Speed (Mbps)')
    ax1.set_title('Download Speed Test Results')
    ax1.legend()

    ax2.set_xlabel('Test Number')
    ax2.set_ylabel('Upload Speed (Mbps)')
    ax2.set_title('Upload Speed Test Results')
    ax2.legend()

    # Adjusting layout and showing the plots
    plt.tight_layout()
    plt.show()

    # Saving plots as images
    fig.savefig('download_upload_speeds.png')


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python speedtest.py <number_of_runs>")
        sys.exit(1)

    num_runs = int(sys.argv[1])

    download_speeds, upload_speeds = [], []
    latencies, jitters, lows, highs = [], [], [], []

    for _ in range(num_runs):
        output = run_speedtest()
        data = extract_data(output)

        download_speeds.append(data['download'])
        upload_speeds.append(data['upload'])
        latencies.append(data['latency'])
        jitters.append(data['jitter'])
        lows.append(data['low'])
        highs.append(data['high'])

        # Print results
        print(f"Download Speeds: {data['download']}, Upload Speeds: {data['upload']}, Latency: {data['latency']}, Jitter: {data['jitter']}, Low: {data['low']}, High: {data['high']}")

    # Calculate and print averages
    avg_download = sum(download_speeds) / num_runs
    avg_upload = sum(upload_speeds) / num_runs
    avg_latency = sum(latencies) / num_runs
    avg_jitter = sum(jitters) / num_runs
    avg_low = sum(lows) / num_runs
    avg_high = sum(highs) / num_runs

    print(f"Average Download Speed: {avg_download:.2f} Mbps")
    print(f"Average Upload Speed: {avg_upload:.2f} Mbps")
    print(f"Average Latency: {avg_latency:.2f} ms")
    print(f"Average Jitter: {avg_jitter:.2f} ms")
    print(f"Average Low: {avg_low:.2f} ms")
    print(f"Average High: {avg_high:.2f} ms")

    plot_speeds(download_speeds, upload_speeds)


if __name__ == "__main__":
    main()
