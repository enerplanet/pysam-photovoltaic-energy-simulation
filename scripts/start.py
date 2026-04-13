import json
import logging
import glob
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from main import PvPowerGeneration

# Load environment variables and cast paths
load_dotenv()
merra_base_directory = Path(os.environ["merra_base_directory"])
output_path = Path(os.environ["output_path"])

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('pv_service')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/start', methods=['POST'])
def start_simulation():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Resolve country-specific MERRA directory
    country = data.get("country")
    if not country:
        return jsonify({"error": "Missing required 'country' field"}), 400

    country = country.lower().replace(" ", "_")

    # Map native-language and alternate country names to MERRA directory keys
    COUNTRY_ALIASES = {
        # German
        "deutschland": "germany",
        "frankreich": "france",
        "oesterreich": "austria",
        "osterreich": "austria",
        "österreich": "austria",
        "schweiz": "switzerland",
        "niederlande": "netherlands",
        "belgien": "belgium",
        "polen": "poland",
        "schweden": "sweden",
        "norwegen": "norway",
        "finnland": "finland",
        "dänemark": "denmark",
        "daenemark": "denmark",
        "irland": "ireland",
        "tschechien": "czechia",
        "tschechische_republik": "czechia",
        "rumänien": "romania",
        "rumaenien": "romania",
        "ungarn": "hungary",
        "griechenland": "greece",
        "kroatien": "croatia",
        "bulgarien": "bulgaria",
        "slowakei": "slovakia",
        "slowenien": "slovenia",
        "luxemburg": "luxembourg",
        "estland": "estonia",
        "lettland": "latvia",
        "litauen": "lithuania",
        "spanien": "spain",
        "italien": "italy",
        "portugal": "portugal",
        # English alternates
        "czechia": "czechia",
        "united_kingdom": "uk",
        "great_britain": "uk",
        "the_netherlands": "netherlands",
        "holland": "netherlands",
        # French
        "allemagne": "germany",
        "autriche": "austria",
        "suisse": "switzerland",
        "pays-bas": "netherlands",
        "pays_bas": "netherlands",
        "belgique": "belgium",
        "pologne": "poland",
        "suède": "sweden",
        "suede": "sweden",
        "norvège": "norway",
        "norvege": "norway",
        "finlande": "finland",
        "danemark": "denmark",
        "irlande": "ireland",
        "tchéquie": "czechia",
        "tchequie": "czechia",
        "république_tchèque": "czechia",
        "republique_tcheque": "czechia",
        "roumanie": "romania",
        "hongrie": "hungary",
        "grèce": "greece",
        "grece": "greece",
        "croatie": "croatia",
        "bulgarie": "bulgaria",
        "slovaquie": "slovakia",
        "slovénie": "slovenia",
        "slovenie": "slovenia",
        "estonie": "estonia",
        "lettonie": "latvia",
        "lituanie": "lithuania",
        "espagne": "spain",
        "italie": "italy",
        "royaume-uni": "uk",
        "royaume_uni": "uk",
    }
    country = COUNTRY_ALIASES.get(country, country)

    merra_directory = merra_base_directory / country
    if not merra_directory.exists():
        logger.error(f"No MERRA data directory found: {merra_directory}")
        return jsonify({"error": f"No MERRA data found for country: {country}"}), 400

    start_date = data.get("start_date")
    end_date = data.get("end_date")
    if not all([start_date, end_date]):
        return jsonify({"error": "Missing required date parameters"}), 400

    # Use model_id for output isolation; fall back to UUID for safety
    model_id = data.get("model_id")
    if model_id is None:
        model_id = str(uuid.uuid4())[:8]
    model_id = str(model_id)

    # Create model-specific output directory
    model_output_path = output_path / model_id
    os.makedirs(model_output_path, exist_ok=True)

    # Clean up old PV files only in this model's directory
    pattern = f'{model_output_path}{os.sep}pv_*'
    for file in glob.glob(pattern):
        try:
            os.remove(file)
        except OSError as e:
            logger.error(f'Error removing old output file: {file}: {e}')

    # Find first POI with pv_supply to get constructor defaults
    pv_supply = None
    for feature in data.get('topology', []):
        for poi_key in ["from", "to"]:
            poi = feature.get(poi_key, {})
            techs = poi.get('techs', {})
            if techs and 'pv_supply' in techs:
                pv_supply = techs['pv_supply']
                break
        if pv_supply:
            break

    if not pv_supply:
        return jsonify({"error": "No valid PV configurations found in topology"}), 400

    try:
        pv_power_generation = PvPowerGeneration(
            start_date=start_date,
            end_date=end_date,
            merra_directory=merra_directory,
            output_path=model_output_path,
            system_capacity=float(pv_supply.get('system_capacity', 6)),
            azimuth=float(pv_supply.get('azimuth', 180)),
            tilt=float(pv_supply.get('tilt', 35)),
            inv_eff=float(pv_supply.get('inv_eff', 0.96)),
            losses=float(pv_supply.get('losses', 0.14)),
            dc_ac_ratio=float(pv_supply.get('dc_ac_ratio', 1.1)),
            module_type=int(pv_supply.get('module_type', 0))
        )
        result = pv_power_generation.run(data=data)
    except Exception as e:
        logger.error(f"Error during simulation: {str(e)}")
        return jsonify({"error": str(e)}), 500

    status_code = result.get('status_code', 200)
    return jsonify(result), status_code


if __name__ == '__main__':
    # For local development only; production uses Gunicorn
    app.run(host='0.0.0.0', port=8082, debug=False)