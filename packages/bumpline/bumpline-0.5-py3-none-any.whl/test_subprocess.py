import subprocess as sp


def test_subprocess(mocker):
    mock_ls = mocker.patch("subprocess.run")
    mock_ls.return_value.stdout = b""
    mock_ls.return_value.returncode = 0

    result = sp.run(["ls"], stdout=sp.PIPE)

    assert result.stdout == b""
    assert result.returncode == 0
