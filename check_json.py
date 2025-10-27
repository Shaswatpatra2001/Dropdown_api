import json

def check_json_structure():
    try:
        with open('data/locations.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print("=== JSON STRUCTURE ANALYSIS ===")
        print(f"📊 Root data type: {type(data)}")
        
        if isinstance(data, dict):
            print("🗺️ Structure: DICTIONARY")
            states = list(data.keys())
            print(f"📋 Number of states: {len(states)}")
            print(f"🎯 States: {states}")
            
            if states:
                first_state = states[0]
                print(f"\n🔍 Examining first state: '{first_state}'")
                state_data = data[first_state]
                print(f"📁 State data type: {type(state_data)}")
                
                if isinstance(state_data, dict):
                    districts = state_data.get('districts', {})
                    print(f"🏛️ Districts type: {type(districts)}")
                    
                    if isinstance(districts, dict):
                        district_names = list(districts.keys())
                        print(f"📋 Number of districts: {len(district_names)}")
                        print(f"🎯 Districts: {district_names[:5]}...")  # First 5
                        
                        if district_names:
                            first_district = district_names[0]
                            print(f"\n🔍 Examining first district: '{first_district}'")
                            district_data = districts[first_district]
                            print(f"📁 District data type: {type(district_data)}")
                            
                            if isinstance(district_data, dict):
                                blocks = district_data.get('blocks', {})
                                print(f"🏘️ Blocks type: {type(blocks)}")
                                
                                if isinstance(blocks, dict):
                                    block_names = list(blocks.keys())
                                    print(f"📋 Number of blocks: {len(block_names)}")
                                    print(f"🎯 Blocks: {block_names[:5]}...")  # First 5
                                    
                                    if block_names:
                                        first_block = block_names[0]
                                        print(f"\n🔍 Examining first block: '{first_block}'")
                                        block_data = blocks[first_block]
                                        print(f"📁 Block data type: {type(block_data)}")
                                        
                                        if isinstance(block_data, list):
                                            print(f"🏡 Number of villages: {len(block_data)}")
                                            print(f"🎯 First 5 villages: {block_data[:5]}")
                                        else:
                                            print(f"❌ Block data is not a list: {type(block_data)}")
                                else:
                                    print(f"❌ Blocks is not a dict: {type(blocks)}")
                            else:
                                print(f"❌ District data is not a dict: {type(district_data)}")
                    else:
                        print(f"❌ Districts is not a dict: {type(districts)}")
                else:
                    print(f"❌ State data is not a dict: {type(state_data)}")
        
        elif isinstance(data, list):
            print("🗺️ Structure: LIST")
            print(f"📋 Number of items: {len(data)}")
            if data:
                first_item = data[0]
                print(f"🎯 First item type: {type(first_item)}")
                if isinstance(first_item, dict):
                    print(f"🔑 First item keys: {list(first_item.keys())}")
        
        else:
            print(f"❌ Unknown structure: {type(data)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_json_structure()