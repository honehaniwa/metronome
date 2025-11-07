"""メトロノーム音声生成のコアロジック"""

import numpy as np


def generate_click_sound(sample_rate=44100, frequency=1000, duration=0.05):
    """
    クリック音を生成する

    Args:
        sample_rate: サンプリングレート (Hz)
        frequency: クリック音の周波数 (Hz)
        duration: クリック音の長さ (秒)

    Returns:
        numpy.ndarray: クリック音の波形データ
    """
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)

    # サイン波を生成
    wave = np.sin(frequency * 2 * np.pi * t)

    # エンベロープを適用（音の減衰）
    envelope = np.exp(-t * 20)
    wave = wave * envelope

    # 音量を調整（-1.0 ~ 1.0の範囲）
    wave = wave * 0.5

    return wave


def generate_metronome(bpm, duration_seconds=60, sample_rate=44100, pattern="4beat"):
    """
    メトロノームの音声データを生成する

    Args:
        bpm: テンポ（Beats Per Minute）
        duration_seconds: 生成する音声の長さ（秒）
        sample_rate: サンプリングレート (Hz)
        pattern: リズムパターン（"4beat" or "4to8"）
                 "4beat": 通常の4つ打ち
                 "4to8": 4つ打ち2小節→8つ打ち1小節（12拍1サイクル）

    Returns:
        numpy.ndarray: メトロノームの波形データ（16ビット整数）
    """
    if pattern == "4to8":
        return _generate_4to8_pattern(bpm, duration_seconds, sample_rate)
    else:
        return _generate_4beat_pattern(bpm, duration_seconds, sample_rate)


def _generate_4beat_pattern(bpm, duration_seconds, sample_rate):
    """通常の4つ打ちパターンを生成"""
    # 1拍の間隔を計算（秒）
    beat_interval = 60.0 / bpm

    # 通常のクリック音（2〜4拍目用）
    click_normal = generate_click_sound(sample_rate, frequency=800)

    # 頭拍用のクリック音（1拍目用、少し高い音）
    click_accent = generate_click_sound(sample_rate, frequency=1600)

    click_samples = len(click_normal)

    # 4拍で1サイクル
    cycle_beats = 4
    cycle_duration = beat_interval * cycle_beats

    # 指定秒数以上で1サイクル完結するサイクル数を計算
    num_cycles = int(duration_seconds / cycle_duration)
    if duration_seconds % cycle_duration > 0:
        num_cycles += 1  # 余りがある場合は1サイクル追加

    # 実際の長さを計算（1サイクル完結）
    actual_duration = num_cycles * cycle_duration
    total_samples = int(sample_rate * actual_duration)

    # 空の波形を作成
    metronome_wave = np.zeros(total_samples)

    current_time = 0.0

    for cycle in range(num_cycles):
        for beat in range(4):
            position = int(current_time * sample_rate)

            # 1拍目は高い音を使用
            if beat == 0:
                current_click = click_accent
            else:
                current_click = click_normal

            # 範囲チェック
            if position + click_samples <= total_samples:
                metronome_wave[position:position + click_samples] += current_click

            current_time += beat_interval

    # クリッピング防止
    metronome_wave = np.clip(metronome_wave, -1.0, 1.0)

    # 16ビット整数に変換
    metronome_wave = (metronome_wave * 32767).astype(np.int16)

    return metronome_wave


def _generate_4to8_pattern(bpm, duration_seconds, sample_rate):
    """
    4つ打ち→8つ打ちを2拍ずつ交互に繰り返すパターンを生成
    1サイクル = 8拍
    - 1〜2拍目: 4つ打ち（2回）
    - 3〜4拍目: 8つ打ち（4回、倍速）
    - 5〜6拍目: 4つ打ち（2回）
    - 7〜8拍目: 8つ打ち（4回、倍速）
    """
    # 1拍の間隔を計算（秒）
    beat_interval = 60.0 / bpm

    # 通常のクリック音（2〜4拍目用）
    click_normal = generate_click_sound(sample_rate, frequency=800)

    # 頭拍用のクリック音（1拍目用、少し高い音）
    click_accent = generate_click_sound(sample_rate, frequency=1600)

    click_samples = len(click_normal)

    # 8拍で1サイクル
    cycle_beats = 8
    cycle_duration = beat_interval * cycle_beats

    # 指定秒数以上で1サイクル完結するサイクル数を計算
    num_cycles = int(duration_seconds / cycle_duration)
    if duration_seconds % cycle_duration > 0:
        num_cycles += 1  # 余りがある場合は1サイクル追加

    # 実際の長さを計算（1サイクル完結）
    actual_duration = num_cycles * cycle_duration
    total_samples = int(sample_rate * actual_duration)

    # 空の波形を作成
    metronome_wave = np.zeros(total_samples)

    current_time = 0.0

    for cycle in range(num_cycles):
        # セグメント1: 4つ打ち2拍（2回）
        for beat in range(2):
            position = int(current_time * sample_rate)

            # 1拍目にアクセント
            if beat == 0:
                current_click = click_accent
            else:
                current_click = click_normal

            if position + click_samples <= total_samples:
                metronome_wave[position:position + click_samples] += current_click

            current_time += beat_interval

        # セグメント2: 8つ打ち4つ（2拍分、倍速）
        half_interval = beat_interval / 2
        for beat in range(4):
            position = int(current_time * sample_rate)

            # 8つ打ちは全て通常音
            current_click = click_normal

            if position + click_samples <= total_samples:
                metronome_wave[position:position + click_samples] += current_click

            current_time += half_interval

        # セグメント3: 4つ打ち2拍（2回）
        for beat in range(2):
            position = int(current_time * sample_rate)

            # 1拍目にアクセント
            if beat == 0:
                current_click = click_accent
            else:
                current_click = click_normal

            if position + click_samples <= total_samples:
                metronome_wave[position:position + click_samples] += current_click

            current_time += beat_interval

        # セグメント4: 8つ打ち4つ（2拍分、倍速）
        for beat in range(4):
            position = int(current_time * sample_rate)

            # 8つ打ちは全て通常音
            current_click = click_normal

            if position + click_samples <= total_samples:
                metronome_wave[position:position + click_samples] += current_click

            current_time += half_interval

    # クリッピング防止
    metronome_wave = np.clip(metronome_wave, -1.0, 1.0)

    # 16ビット整数に変換
    metronome_wave = (metronome_wave * 32767).astype(np.int16)

    return metronome_wave
