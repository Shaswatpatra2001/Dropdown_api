import json
import os
import sys

# Add the project to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def explore_json():
    """Explore the exact structure of your JSON file"""
    try:
        json_path = 'data/locations.json'
        print(f"📁 Looking for JSON file at: {os.path.abspath(json_path)}")
        print(f"📄 File exists: {os.path.exists(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print("=" * 70)
        print("🔍 JSON STRUCTURE EXPLORER - DETAILED ANALYSIS")
        print("=" * 70)
        
        def explore(obj, path="", depth=0):
            indent = "  " * depth
            if depth > 4:  # Limit depth to avoid too much output
                return
                
            if isinstance(obj, dict):
                if depth == 0:
                    print(f"{indent}🏠 ROOT LEVEL")
                    print(f"{indent}📊 Type: dict")
                    print(f"{indent}🔑 Number of keys: {len(obj)}")
                    print(f"{indent}🎯 All keys: {list(obj.keys())}")
                    print("-" * 50)
                
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    
                    # Print based on depth level
                    if depth == 0:
                        print(f"{indent}🗺️ STATE: '{key}'")
                        print(f"{indent}  📁 Data type: {type(value)}")
                    elif depth == 1:
                        print(f"{indent}  🏛️ DISTRICT: '{key}'")
                        print(f"{indent}    📁 Data type: {type(value)}")
                    elif depth == 2:
                        print(f"{indent}    🏘️ BLOCK: '{key}'")
                        print(f"{indent}      📁 Data type: {type(value)}")
                    elif depth == 3:
                        print(f"{indent}      🏡 VILLAGE LEVEL")
                        print(f"{indent}        📁 Data type: {type(value)}")
                    
                    # Explore deeper if it's a container type
                    if isinstance(value, (dict, list)) and depth < 3:
                        explore(value, new_path, depth + 1)
                    
                    # Special handling for village data
                    elif depth == 2 and isinstance(value, dict):
                        # Check if this block has villages directly or needs deeper exploration
                        if 'villages' in value:
                            villages = value['villages']
                            print(f"{indent}      🏡 Found 'villages' key")
                            print(f"{indent}        📋 Number of villages: {len(villages) if isinstance(villages, list) else 'N/A'}")
                            if isinstance(villages, list) and villages:
                                print(f"{indent}        🎯 First 3 villages: {villages[:3]}")
                        else:
                            # If no villages key, maybe villages are directly in the block
                            print(f"{indent}      🔍 Block keys: {list(value.keys())}")
                    
                    elif depth == 2 and isinstance(value, list):
                        print(f"{indent}      📋 Block contains list with {len(value)} items")
                        if value and isinstance(value[0], dict):
                            print(f"{indent}        🔑 First item keys: {list(value[0].keys())}")
                            
            elif isinstance(obj, list):
                print(f"{indent}📋 LIST with {len(obj)} items")
                if obj and depth < 3:
                    print(f"{indent}🔍 First item type: {type(obj[0])}")
                    if isinstance(obj[0], dict):
                        print(f"{indent}🎯 First item keys: {list(obj[0].keys())}")
                    explore(obj[0], f"{path}[0]", depth + 1)
        
        explore(data)
        
        print("\n" + "=" * 70)
        print("🎯 SPECIFIC SEARCH FOR ODISHA -> KHORDA -> JANKIA")
        print("=" * 70)
        
        # Let's specifically search for the path we need
        if isinstance(data, dict) and 'odisha' in data:
            odisha_data = data['odisha']
            print("✅ Found 'odisha' state")
            if isinstance(odisha_data, dict) and 'districts' in odisha_data:
                districts_data = odisha_data['districts']
                print("✅ Found 'districts' in odisha")
                if isinstance(districts_data, dict) and 'khordha' in districts_data:
                    khordha_data = districts_data['khordha']
                    print("✅ Found 'khordha' district")
                    if isinstance(khordha_data, dict) and 'blocks' in khordha_data:
                        blocks_data = khordha_data['blocks']
                        print("✅ Found 'blocks' in khordha")
                        if isinstance(blocks_data, dict) and 'jankia' in blocks_data:
                            jankia_data = blocks_data['jankia']
                            print("🎉 SUCCESS: Found 'jankia' block!")
                            print(f"📁 Jankia data type: {type(jankia_data)}")
                            if isinstance(jankia_data, list):
                                print(f"🏡 Number of villages in Jankia: {len(jankia_data)}")
                                print(f"🎯 First 5 villages: {jankia_data[:5]}")
                            else:
                                print(f"❓ Jankia data is not a list: {type(jankia_data)}")
                        else:
                            print("❌ 'jankia' not found in blocks")
                            print(f"🔍 Available blocks: {list(blocks_data.keys()) if isinstance(blocks_data, dict) else 'N/A'}")
                    else:
                        print("❌ 'blocks' not found in khordha")
                        print(f"🔍 Khordha keys: {list(khordha_data.keys()) if isinstance(khordha_data, dict) else 'N/A'}")
                else:
                    print("❌ 'khordha' not found in districts")
                    print(f"🔍 Available districts: {list(districts_data.keys()) if isinstance(districts_data, dict) else 'N/A'}")
            else:
                print("❌ 'districts' not found in odisha")
                print(f"🔍 Odisha keys: {list(odisha_data.keys()) if isinstance(odisha_data, dict) else 'N/A'}")
        else:
            print("❌ 'odisha' not found in root data")
            print(f"🔍 Available states: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explore_json()