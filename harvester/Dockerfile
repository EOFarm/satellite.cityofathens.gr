FROM ubuntu:noble

# Install cron, Python, and dependencies
RUN apt-get update && \
    apt-get install -y cron curl bash python3 python3-pip && \
    pip install --break-system-packages prometheus_client \
    pystac==1.14.1 pystac-client==0.9.0 planetary_computer==1.0.0 \
    odc-stac==0.4.0 matplotlib==3.10.6 rioxarray==0.20.0 \
	tqdm==4.67.1 && \
    rm -rf /var/lib/apt/lists/*

# Copy cron job
COPY crontab /etc/cron.d/worker-cron
RUN chmod 0644 /etc/cron.d/worker-cron && crontab /etc/cron.d/worker-cron

# Copy scripts
COPY scripts /usr/local/bin/scripts
COPY collections /collections
RUN chmod +x /usr/local/bin/scripts/*

# Start cron
CMD cron && python3 /usr/local/bin/scripts/metrics_server.py
