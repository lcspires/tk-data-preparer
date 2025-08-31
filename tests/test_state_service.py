# tests/test_state_service.py
import pytest
import pandas as pd
from tk_data_preparer.app.services.state_service import AppState, get_app_state
from tk_data_preparer.core import AppConfig

class TestAppState:
    def test_initial_state(self):
        state = AppState()
        assert not state.has_data
        assert not state.has_processed_data
        assert not state.has_selected_columns
        assert state.current_data is None
        assert state.current_columns == []
        assert state.pipeline_result is None
        
    def test_set_data(self):
        state = AppState()
        test_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        state.set_data(test_data, 'test.csv')
        assert state.has_data
        assert state.initial_rows_count == 2
        assert state.current_filepath == 'test.csv'
        
    def test_set_columns(self):
        state = AppState()
        state.set_columns(['col1', 'col2'])
        assert state.has_selected_columns
        assert state.current_columns == ['col1', 'col2']
        
    def test_reset(self):
        state = AppState()
        test_data = pd.DataFrame({'col1': [1, 2]})
        state.set_data(test_data)
        state.set_columns(['col1'])
        
        state.reset()
        assert not state.has_data
        assert not state.has_selected_columns
        assert state.current_columns == []
        
    def test_observer_pattern(self):
        state = AppState()
        events_received = []
        
        def test_callback(data):
            events_received.append(data)
            
        state.subscribe('data_loaded', test_callback)
        test_data = pd.DataFrame({'col1': [1, 2]})
        state.set_data(test_data)
        
        assert len(events_received) == 1
        assert events_received[0].equals(test_data)
        
    def test_singleton_pattern(self):
        state1 = get_app_state()
        state2 = get_app_state()
        assert state1 is state2
        
        reset_app_state()
        state3 = get_app_state()
        assert state3 is not state1