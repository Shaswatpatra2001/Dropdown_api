import json
import os
from django.conf import settings

class LocationService:
    def __init__(self):
        self.data = self._load_json_data()
        print("=" * 60)
        print("🚀 LOCATION SERVICE INITIALIZED")
        print(f"📊 Data type: {type(self.data)}")
        print("✅ JSON Structure: List of states with 'districts' and 'subDistricts'")
        print("=" * 60)
    
    def _load_json_data(self):
        """Load JSON data from file"""
        try:
            with open(settings.JSON_DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return []

    def get_states(self):
        """Get all states"""
        print(f"\n🎯 GET_STATES called")
        
        states = []
        for item in self.data:
            if isinstance(item, dict):
                state_name = item.get('state')
                if state_name:
                    states.append(state_name)
        
        print(f"✅ Returning {len(states)} states: {states[:5]}...")  # Show first 5
        return states

    def get_districts(self, state):
        """Get districts for a state"""
        print(f"\n🎯 GET_DISTRICTS called: state='{state}'")
        
        state_lower = state.lower().strip()
        
        for state_item in self.data:
            if isinstance(state_item, dict):
                item_state = state_item.get('state')
                if item_state and item_state.lower() == state_lower:
                    print(f"✅ Found state: '{item_state}'")
                    
                    districts_data = state_item.get('districts', [])
                    districts = []
                    
                    for dist_item in districts_data:
                        if isinstance(dist_item, dict):
                            dist_name = dist_item.get('district')
                            if dist_name:
                                districts.append(dist_name)
                    
                    print(f"✅ Found {len(districts)} districts: {districts[:5]}...")
                    return districts
        
        print(f"❌ No districts found for state: {state}")
        return []

    def get_blocks(self, state, district):
        """Get blocks (subDistricts) for a district"""
        print(f"\n🎯 GET_BLOCKS called: state='{state}', district='{district}'")
        
        state_lower = state.lower().strip()
        district_lower = district.lower().strip()
        
        for state_item in self.data:
            if isinstance(state_item, dict):
                item_state = state_item.get('state')
                if item_state and item_state.lower() == state_lower:
                    print(f"✅ Found state: '{item_state}'")
                    
                    districts_data = state_item.get('districts', [])
                    
                    for dist_item in districts_data:
                        if isinstance(dist_item, dict):
                            dist_name = dist_item.get('district')
                            if dist_name and dist_name.lower() == district_lower:
                                print(f"✅ Found district: '{dist_name}'")
                                
                                # In your JSON, blocks are called 'subDistricts'
                                subdistricts_data = dist_item.get('subDistricts', [])
                                blocks = []
                                
                                for subdist_item in subdistricts_data:
                                    if isinstance(subdist_item, dict):
                                        block_name = subdist_item.get('subDistrict')
                                        if block_name:
                                            blocks.append(block_name)
                                
                                print(f"✅ Found {len(blocks)} blocks (subDistricts): {blocks[:5]}...")
                                return blocks
        
        print(f"❌ No blocks found for {district}, {state}")
        return []

    def get_villages(self, state, district, block):
        """Get villages for a block (subDistrict)"""
        print(f"\n🎯 GET_VILLAGES called: state='{state}', district='{district}', block='{block}'")
        
        state_lower = state.lower().strip()
        district_lower = district.lower().strip()
        block_lower = block.lower().strip()
        
        for state_item in self.data:
            if isinstance(state_item, dict):
                item_state = state_item.get('state')
                if item_state and item_state.lower() == state_lower:
                    print(f"✅ Found state: '{item_state}'")
                    
                    districts_data = state_item.get('districts', [])
                    
                    for dist_item in districts_data:
                        if isinstance(dist_item, dict):
                            dist_name = dist_item.get('district')
                            if dist_name and dist_name.lower() == district_lower:
                                print(f"✅ Found district: '{dist_name}'")
                                
                                subdistricts_data = dist_item.get('subDistricts', [])
                                
                                for subdist_item in subdistricts_data:
                                    if isinstance(subdist_item, dict):
                                        block_name = subdist_item.get('subDistrict')
                                        if block_name and block_name.lower() == block_lower:
                                            print(f"✅ Found block (subDistrict): '{block_name}'")
                                            
                                            # Villages are directly in the subDistrict object as a list
                                            villages = subdist_item.get('villages', [])
                                            print(f"✅ Found {len(villages)} villages: {villages[:5]}...")
                                            return villages
        
        print(f"❌ No villages found for {block}, {district}, {state}")
        return []

# Create global instance
location_service = LocationService()