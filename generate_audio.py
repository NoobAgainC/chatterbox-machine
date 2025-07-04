import argparse
import torch
import torchaudio as ta

from chatterbox.vc import ChatterboxVC

def main():
    # How to execute this script from the terminal:
    # ----------------------------------------------
    # Basic usage (generate audio from text file):
    #     python generate_audio.py input.txt
    #
    # Specify an audio sample for voice cloning:
    #     python generate_audio.py input.txt --voice_sample sample.wav
    #
    # Specify output file name:
    #     python generate_audio.py input.txt --voice_sample sample.wav --output result.wav
    #
    # All arguments:
    #   input.txt              Path to the text file containing text to synthesize (required)
    #   --voice_sample FILE    Optional path to an audio file for voice cloning
    #   -o, --output FILE      Output path for generated audio (default: output.wav)
    # ----------------------------------------------

    # 1. Parse command-line arguments for text file, optional voice sample, and output path
    parser = argparse.ArgumentParser(
        description="Generate audio from a text file using ChatterboxVC. Optionally provide an audio sample for voice cloning."
    )
    parser.add_argument(
        "textfile",
        type=str,
        help="Path to the text file containing the text to synthesize."
    )
    parser.add_argument(
        "--voice_sample",
        type=str,
        default=None,
        help="Optional path to an audio file for voice cloning. If not provided, a default voice will be used."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.wav",
        help="Path to save the generated audio (default: output.wav)."
    )
    args = parser.parse_args()

    # 2. Select the best available device (GPU, MPS, or CPU)
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print(f"Using device: {device}")

    # 3. Read the contents of the input text file
    with open(args.textfile, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # 4. Load the ChatterboxVC model with the selected device
    model = ChatterboxVC.from_pretrained(device)

    # 5. Generate audio from the input text and (optional) voice sample
    wav = model.generate(
        text=text,
        target_voice_path=args.voice_sample
    )

    # 6. Save the generated audio to the specified output file
    ta.save(args.output, wav, model.sr)
    print(f"Audio saved to {args.output}")

if __name__ == "__main__":
    main()
