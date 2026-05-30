import sys
from unittest.mock import MagicMock, Mock, patch

import pytest


class TestMainDispatch:
    def test_produce_help(self):
        with patch.object(sys, "argv", ["main.py", "produce", "--help"]):
            with pytest.raises(SystemExit) as exc:
                import src.main
                src.main.main()
            assert exc.value.code == 0

    def test_consume_help(self):
        with patch.object(sys, "argv", ["main.py", "consume", "--help"]):
            with pytest.raises(SystemExit) as exc:
                import src.main
                src.main.main()
            assert exc.value.code == 0

    def test_serve_help(self):
        with patch.object(sys, "argv", ["main.py", "serve", "--help"]):
            with pytest.raises(SystemExit) as exc:
                import src.main
                src.main.main()
            assert exc.value.code == 0

    def test_main_no_args_shows_help(self):
        with patch.object(sys, "argv", ["main.py"]):
            with pytest.raises(SystemExit) as exc:
                import src.main
                src.main.main()
            assert exc.value.code == 2

    @patch("src.main._cmd_produce")
    def test_produce_dispatches(self, mock_cmd):
        with patch.object(sys, "argv", ["main.py", "produce", "--amount", "200", "--card", "X", "--restaurant", "R"]):
            import src.main
            src.main.main()
            mock_cmd.assert_called_once_with(amount=200.0, card_number="X", restaurant_code="R")

    @patch("src.main._cmd_consume")
    def test_consume_dispatches(self, mock_cmd):
        with patch.object(sys, "argv", ["main.py", "consume"]):
            import src.main
            src.main.main()
            mock_cmd.assert_called_once()

    @patch("src.main._cmd_serve")
    def test_serve_dispatches(self, mock_cmd):
        with patch.object(sys, "argv", ["main.py", "serve", "--port", "9000"]):
            import src.main
            src.main.main()
            mock_cmd.assert_called_once_with(9000)


class TestCmdProduce:
    @patch("src.main.RabbitMQAdapter")
    def test_produce_creates_transaction_and_publishes(self, mock_adapter_cls):
        mock_adapter = mock_adapter_cls.return_value
        import src.main
        src.main._cmd_produce(amount=300.0, card_number="4111-1111-1111-1111", restaurant_code="REST-099")
        mock_adapter_cls.assert_called_once()
        assert mock_adapter.publish.call_count == 1
        assert mock_adapter.close.call_count == 1


class TestCmdConsume:
    @patch("src.main.RabbitMQConsumerAdapter")
    @patch("src.main.ProcessRewardUseCase")
    @patch("src.main.InMemoryRewardRepository")
    def test_consume_creates_consumer_and_starts(self, mock_repo_cls, mock_uc_cls, mock_consumer_cls):
        mock_consumer = mock_consumer_cls.return_value
        import src.main
        src.main._cmd_consume()
        mock_repo_cls.assert_called_once()
        mock_uc_cls.assert_called_once()
        mock_consumer_cls.assert_called_once()
        mock_consumer.start.assert_called_once()

    @patch("src.main.RabbitMQConsumerAdapter")
    @patch("src.main.ProcessRewardUseCase")
    @patch("src.main.InMemoryRewardRepository")
    def test_consume_handles_keyboard_interrupt(self, mock_repo_cls, mock_uc_cls, mock_consumer_cls):
        mock_consumer = mock_consumer_cls.return_value
        mock_consumer.start.side_effect = KeyboardInterrupt()
        import src.main
        src.main._cmd_consume()
        mock_consumer.close.assert_called_once()


class TestCmdServe:
    @patch("src.main.uvicorn")
    def test_serve_runs_uvicorn_with_localhost(self, mock_uvicorn):
        import src.main
        src.main._cmd_serve(port=8000)
        mock_uvicorn.run.assert_called_once_with(
            "src.costumerProducer.infraestructure.api:app",
            host="127.0.0.1",
            port=8000,
        )
