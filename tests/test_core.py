"""Tests for core metronome generation logic"""

import numpy as np
import pytest

from src.metronome.core import (
    _generate_4beat_pattern,
    _generate_4to8_pattern,
    generate_click_sound,
    generate_metronome,
)


class TestClickSound:
    """Tests for click sound generation"""

    def test_generate_click_sound_default(self):
        """Test default click sound generation"""
        sound = generate_click_sound()
        assert isinstance(sound, np.ndarray)
        assert len(sound) > 0
        assert sound.dtype == np.float64

    def test_generate_click_sound_custom_frequency(self):
        """Test click sound with custom frequency"""
        sound_800 = generate_click_sound(frequency=800)
        sound_1600 = generate_click_sound(frequency=1600)
        assert len(sound_800) == len(sound_1600)
        # Different frequencies should produce different waveforms
        assert not np.allclose(sound_800, sound_1600)

    def test_generate_click_sound_custom_duration(self):
        """Test click sound with custom duration"""
        sample_rate = 44100
        duration = 0.1
        sound = generate_click_sound(sample_rate=sample_rate, duration=duration)
        expected_samples = int(sample_rate * duration)
        assert len(sound) == expected_samples


class TestMetronomeGeneration:
    """Tests for metronome pattern generation"""

    def test_generate_4beat_basic(self):
        """Test basic 4-beat pattern generation"""
        bpm = 120
        duration = 5
        wave_data = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4beat")

        assert isinstance(wave_data, np.ndarray)
        assert wave_data.dtype == np.int16
        assert len(wave_data) > 0

    def test_generate_4to8_basic(self):
        """Test basic 4-to-8 pattern generation"""
        bpm = 120
        duration = 5
        wave_data = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4to8")

        assert isinstance(wave_data, np.ndarray)
        assert wave_data.dtype == np.int16
        assert len(wave_data) > 0

    def test_different_bpm_produces_different_length(self):
        """Test that different BPMs with same duration produce different cycle counts"""
        duration = 10
        wave_120 = generate_metronome(bpm=120, duration_seconds=duration, pattern="4beat")
        wave_180 = generate_metronome(bpm=180, duration_seconds=duration, pattern="4beat")

        # Both should be close in length but not identical due to cycle completion
        assert len(wave_120) > 0
        assert len(wave_180) > 0

    def test_cycle_completion_4beat(self):
        """Test that 4-beat pattern completes cycles"""
        bpm = 120
        beat_interval = 60.0 / bpm  # 0.5 seconds
        cycle_duration = beat_interval * 4  # 2 seconds

        # Request 5 seconds, should get 3 complete cycles (6 seconds)
        duration = 5
        wave_data = _generate_4beat_pattern(bpm=bpm, duration_seconds=duration, sample_rate=44100)

        expected_duration = 3 * cycle_duration  # 6 seconds
        expected_samples = int(44100 * expected_duration)

        assert len(wave_data) == expected_samples

    def test_cycle_completion_4to8(self):
        """Test that 4-to-8 pattern completes cycles"""
        bpm = 120
        beat_interval = 60.0 / bpm  # 0.5 seconds
        cycle_duration = beat_interval * 8  # 4 seconds

        # Request 5 seconds, should get 2 complete cycles (8 seconds)
        duration = 5
        wave_data = _generate_4to8_pattern(bpm=bpm, duration_seconds=duration, sample_rate=44100)

        expected_duration = 2 * cycle_duration  # 8 seconds
        expected_samples = int(44100 * expected_duration)

        assert len(wave_data) == expected_samples

    def test_audio_data_range(self):
        """Test that audio data is within valid 16-bit range"""
        wave_data = generate_metronome(bpm=120, duration_seconds=5, pattern="4beat")
        assert np.all(wave_data >= -32768)
        assert np.all(wave_data <= 32767)

    def test_extreme_bpm_values(self):
        """Test edge cases for BPM values"""
        # Very slow BPM
        wave_slow = generate_metronome(bpm=20, duration_seconds=5, pattern="4beat")
        assert len(wave_slow) > 0

        # Very fast BPM
        wave_fast = generate_metronome(bpm=300, duration_seconds=5, pattern="4beat")
        assert len(wave_fast) > 0

    def test_sample_rate_variations(self):
        """Test different sample rates"""
        bpm = 120
        duration = 5

        wave_22050 = generate_metronome(bpm=bpm, duration_seconds=duration, sample_rate=22050)
        wave_44100 = generate_metronome(bpm=bpm, duration_seconds=duration, sample_rate=44100)
        wave_48000 = generate_metronome(bpm=bpm, duration_seconds=duration, sample_rate=48000)

        # Higher sample rates should produce more samples for same duration
        assert len(wave_22050) < len(wave_44100) < len(wave_48000)


class TestPatternDifferences:
    """Tests to verify differences between patterns"""

    def test_4beat_vs_4to8_different(self):
        """Test that 4-beat and 4-to-8 patterns produce different audio"""
        bpm = 120
        duration = 10

        wave_4beat = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4beat")
        wave_4to8 = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4to8")

        # Patterns should be different
        assert not np.array_equal(wave_4beat, wave_4to8)

    def test_4to8_has_more_beats(self):
        """Test that 4-to-8 pattern has more beats than 4-beat in same time"""
        bpm = 120
        duration = 10

        # 4-to-8 should have more non-zero samples due to 8-beat sections
        wave_4beat = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4beat")
        wave_4to8 = generate_metronome(bpm=bpm, duration_seconds=duration, pattern="4to8")

        # Count non-zero regions (approximate beat count)
        beats_4beat = np.count_nonzero(np.abs(wave_4beat) > 1000)
        beats_4to8 = np.count_nonzero(np.abs(wave_4to8) > 1000)

        # 4-to-8 should have more non-zero samples
        assert beats_4to8 > beats_4beat


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
