"""Determine the fastest route from a set of origins to a set of destinations, by any transportation method.

Bulk querying of coordinates to determine the fastest transportation route (by distance or duration) from an origin to the closest destination.
"""

__all__ = ["get_wfs_data"]

_available_transport_modes = ["driving", "walking", "cycling", "public transport"]

import subprocess, socket, os

def init_osrm(name, transport_mode="driving", continent="australia-oceania", region="new-zealand", subregion=None, update_roads=False):
    """Creates a docker container with the osrm/osrm-backend image.
    
    Create (or refresh) a docker container with the given name, that is set up to be a high-performance open-source routing engine (OSRM). OpenStreetMap (OSM) data is stored in '~/.osm'.
        
    Args:
        name: The name to give the docker container.
        transport_mode: The type of transportation to be simulating. Options include: 'driving', 'walking' and 'cycling'.
        continent: The name of the continent to be analysing, e.g. "north-america". See https://download.geofabrik.de/ for a list of available continents.
        region: The name of the region to be analysing, e.g. "canada". See https://download.geofabrik.de/{continent}.html for a list of available regions.
        subregion: The name of the subregion to be analysing, e.g. "ontario". Some regions, such as "new-zealand", will not have subregions. See https://download.geofabrik.de/{continent}/{region}.html for a list of available subregions. 
        update_roads: The path to the csv of which will update roads in the OSM network.
    
    Returns:
        An integer which is the port the docker container is running on 
    """

    # Determine where to save all the data files
    osm_directory = os.path.expanduser("~/.osm")

    # Determine free port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()

    lua = {'driving':'car','walking':'foot','cycling':'bicycle'}.get(transport_mode, "car")

    # Stop and remove any existing dockers with this name
    subprocess.run(f'docker stop osrm-{name}'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(f'docker rm osrm-{name}'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Download the data
    pbf_filepath = f'https://download.geofabrik.de/{continent}/{region}{f"/{subregion}" if subregion else ""}-latest.osm.pbf'
    download_process = subprocess.run(f'wget -N {pbf_filepath} -P {osm_directory}'.split(), bufsize=0, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    if not '304 Not Modified' in str(download_process.stderr) or (update_roads != False):
        # Extract and initialise the data
        shell_commands = [
            f'docker run -t -v {osm_directory}:/data osrm/osrm-backend osrm-extract -p /opt/{lua}.lua /data/{subregion if subregion else region}-latest.osm.pbf',
            f'docker run -t -v {osm_directory}:/data osrm/osrm-backend osrm-partition /data/{subregion if subregion else region}-latest.osrm',
            f'docker run -t -v {osm_directory}:/data osrm/osrm-backend osrm-customize /data/{subregion if subregion else region}-latest.osrm{f" --segment-speed-file {update_roads}" if update_roads else ""}',
        ]
        for com in shell_commands:
            subprocess.run(com.split(), stdout=open(os.devnull, 'wb'), stderr=subprocess.STDOUT)

    run_docker = f'docker run -d --name osrm-{name} -t -i -p {port}:5000 -v {osm_directory}:/data osrm/osrm-backend osrm-routed --algorithm mld --max-table-size 100000 /data/{subregion if subregion else region}-latest.osrm'
    subprocess.run(run_docker.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return port

