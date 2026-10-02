# Swarm Pepes — IMD mainnet teaser

Delivered video: **artifacts/video.mp4** (`video/mp4`).

20 seconds; 1080 × 1920 portrait; 30 fps. Browser-compatible H.264, yuv420p, AAC stereo at 44.1 kHz, with the MP4 metadata at the front for streaming. Original synthesized chiptune at 120 BPM, bass, kick, rising transition tone and soft coin-flip tings. No third-party music or assets.

The four sequences follow the requested timing: solo coin flips (0–4s), nine different frog skins and hats appearing in a grid (4–10s), coins merging with a spinning central coin and testnet-to-mainnet progress (10–15s), then a front-facing mystery coin and “IMD mainnet is coming” / “swarmpepe.xyz” reveal (15–20s). Progress reaches 100% at 15s. The final frog winks and pockets its coin. Coins carry only a question mark; no token logos, prices or financial claims.

Artwork uses a native 270 × 480 pixel canvas enlarged 4× with nearest-neighbor scaling, green phosphor bloom, subtle scanlines and brief transition flickers. Lettering uses an original small pixel font (displayed in uppercase).

Limitations: previous Swarm Pepes videos and NFT artwork were not supplied, so this is an original interpretation of the described style. Frog portraits are custom illustrations, not authenticated collection token images. The provided Ethereum contract is project context; this clip does not query the contract or certify an announcement date. Audio is synthesized, with no live recording.

## Reproduction

Run `python3 src/render.py` from the repository root with Python 3 and FFmpeg (including libx264) available. No Python packages or network access are needed. The renderer writes its intermediate audio to `/tmp` and produces the required MP4 directly.

## Local checks

FFprobe confirmed the duration, dimensions, codecs, pixel format and audio format recorded above. FFmpeg decoded the entire video and audio without errors. A five-frame contact sheet was inspected at 2s, 6s, 12s, 16s and the final frame. The required artifact is below 64 MiB.
