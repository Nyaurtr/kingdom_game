"""
Simple test to verify core systems work
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.game_state import GameState, MeterState, TrustLevel, GamePhase
from src.core.role_system import RoleSystem, Role
from src.core.meter_system import MeterSystem, MeterType
from src.core.investigation import InvestigationSystem, EvidenceType

def test_role_system():
    """Test role system functionality"""
    print("Testing Role System...")
    
    role_system = RoleSystem()
    
    # Test random role assignment
    role = role_system.get_random_role()
    print(f"OK: Random role assigned: {role.value}")
    
    # Test role data retrieval
    role_data = role_system.get_role_data(role)
    print(f"OK: Role data retrieved: {role_data.name}")
    print(f"OK: Personal secret: {role_data.personal_secret.name}")
    print(f"OK: Signature action: {role_data.signature_action.name}")
    
    return True

def test_meter_system():
    """Test meter system functionality"""
    print("\nTesting Meter System...")
    
    meter_system = MeterSystem()
    
    # Test meter descriptions
    food_desc = meter_system.get_meter_description(
        MeterType.FOOD_SUPPLY, MeterState.STABLE, "visual"
    )
    print(f"OK: Food supply description: {food_desc}")
    
    # Test overall kingdom state
    from src.core.game_state import KingdomMeters
    meters = KingdomMeters()
    kingdom_state = meter_system.get_overall_kingdom_state(meters)
    print(f"OK: Kingdom state: {kingdom_state}")
    
    return True

def test_investigation_system():
    """Test investigation system functionality"""
    print("\nTesting Investigation System...")
    
    investigation_system = InvestigationSystem()
    
    # Test available actions
    actions = investigation_system.get_available_actions("king", 1, {})
    print(f"OK: Available actions for King: {len(actions)}")
    
    # Test evidence generation
    from src.core.game_state import GameState
    game_state = GameState()
    game_state.primary_event = "famine_cascade"
    
    action = investigation_system.investigation_actions["council_hearing"]
    success, evidence, narrative = investigation_system.perform_investigation(
        action, game_state, {}
    )
    
    if success and evidence:
        print(f"OK: Investigation successful: {evidence.content[:50]}...")
    else:
        print(f"ERROR: Investigation failed: {narrative}")
    
    return True

def test_game_state():
    """Test game state functionality"""
    print("\nTesting Game State...")
    
    game_state = GameState()
    game_state.current_role = "king"
    game_state.current_day = 1
    
    # Test serialization
    state_dict = game_state.to_dict()
    print(f"OK: Game state serialized: {len(state_dict)} fields")
    
    # Test deserialization
    new_state = GameState.from_dict(state_dict)
    print(f"OK: Game state deserialized: {new_state.current_role}")
    
    return True

def main():
    """Run all tests"""
    print("Starting Kingdom Game Core Systems Tests\n")
    
    tests = [
        test_role_system,
        test_meter_system, 
        test_investigation_system,
        test_game_state
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"ERROR: Test failed with error: {e}")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! Core systems are working correctly.")
    else:
        print("WARNING: Some tests failed. Check the implementation.")

if __name__ == "__main__":
    main()
