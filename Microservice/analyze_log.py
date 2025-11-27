import json

def analyze_log(filename):
    totalRequests = 0
    counts = {}
    success = 0
    responseTimeSum = 0

    for line in open(filename):
        try:
            method, endpoint, status, time = line.split()
        except ValueError:
            continue

        status = int(status)
        time = int(time.replace("ms", ""))

        totalRequests += 1
        counts[endpoint] = counts.get(endpoint, 0) + 1

        if 200 <= status <= 299:
            success += 1

        responseTimeSum += time

    successRate = (success / totalRequests) * 100
    averageResponseTime = int(responseTimeSum / totalRequests)
    mostFrequentEndpoint = max(counts, key=counts.get)

    summary = {
        "totalRequests": totalRequests,
        "successRate": successRate,
        "averageResponseTime": averageResponseTime,
        "mostFrequentEndpoint": mostFrequentEndpoint
    }

    return summary
