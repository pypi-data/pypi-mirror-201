from click.testing import CliRunner

from codx.cli import main


class TestCli:
    def test_main_gene_ids(self):
        runner = CliRunner()
        result = runner.invoke(main, ["11047"])
        assert result.exit_code == 0

    def test_main_uniprot(self):
        runner = CliRunner()
        result = runner.invoke(main, ["P04637", "--uniprot"])
        assert result.exit_code == 0

    def test_main_translate(self):
        runner = CliRunner()
        result = runner.invoke(main, ["11047", "--translate"])
        assert result.exit_code == 0

    def test_main_three_frame_translate(self):
        runner = CliRunner()
        result = runner.invoke(main, ["11047", "-3"])
        assert result.exit_code == 0