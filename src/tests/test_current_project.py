from fgmk import current_project

def test_current_project():
    assert "gamefolder" in current_project.settings
