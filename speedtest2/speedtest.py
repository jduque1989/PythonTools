import subprocess
import re
import matplotlib.pyplot as plt
import sys


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
    plt.plot(download_speeds, label='Download Speeds (Mbps)')
    plt.plot(upload_speeds, label='Upload Speeds (Mbps)')
    plt.xlabel('Test Number')
    plt.ylabel('Speed (Mbps)')
    plt.title('Internet Speed Test Results')
    plt.legend()
    plt.show()


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
