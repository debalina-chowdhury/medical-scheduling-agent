def test_tools_defined():
    """Test all scheduling tools are defined"""
    from app import tools
    tool_names = [t["name"] for t in tools]
    assert "find_provider" in tool_names
    assert "verify_patient_eligibility" in tool_names
    assert "book_appointment" in tool_names
    assert "process_referral" in tool_names

def test_find_provider():
    """Test find provider returns results"""
    from app import execute_tool
    result = execute_tool("find_provider", {"specialty": "cardiology"})
    assert "DR00" in result
    assert "cardiology" in result.lower()

def test_book_appointment():
    """Test booking returns confirmation"""
    from app import execute_tool
    result = execute_tool("book_appointment", {
        "patient_id": "P001",
        "provider_id": "DR001",
        "appointment_time": "Monday 9am"
    })
    assert "P001" in result
    assert "DR001" in result

def test_verify_eligibility():
    """Test eligibility check returns status"""
    from app import execute_tool
    result = execute_tool("verify_patient_eligibility", {
        "patient_id": "P001",
        "provider_id": "DR001"
    })
    assert "eligible" in result.lower()