import os
import uuid


NODE_ID = str(uuid.uuid1())
MAX_MEMORY=os.getenv("MAX_MEMORY", "1G")
MAX_MEMORY_PER_NODE=os.getenv("MAX_MEMORY_PER_NODE", "1G")
DISCOVERY_URI=os.getenv("DISCOVERY_URI", "http://localhost:8585")


os.makedirs("catalog")


def save_file(file_path, content):
	with open("etc/jvm.config", "r") as f:
		f.write(content)

content=f"""-server
-Xmx16G
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+UseGCOverheadLimit
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError"""


save_file("jvm.config", content)

content = f"""com.facebook.presto=INFO"""

save_file("log.properties", content)


content = f"""coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8585
query.max-memory={MAX_MEMORY}
query.max-memory-per-node=4GB
query.max-total-memory-per-node={MAX_MEMORY_PER_NODE}
discovery-server.enabled=true
discovery.uri={DISCOVERY_URI}"""

save_file("config.properties", content)


content = f"""node.environment=docker
node.id={NODE_ID}
node.data-dir=/app/presto/data
node.launcher-log-file=/app/presto/logs/launcher.log
node.server-log-file=/app/presto/logs/server.log
"""

save_file("node.properties", content)




