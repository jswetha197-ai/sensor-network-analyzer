import matplotlib.pyplot as plt

def generate_plots(df):
    plt.figure()
    plt.hist(df["latency"])
    plt.title("Latency Distribution")
    plt.savefig("visualization/latency.png")

    plt.figure()
    plt.plot(df["node_id"], df["pdr"])
    plt.title("PDR per Node")
    plt.savefig("visualization/pdr.png")