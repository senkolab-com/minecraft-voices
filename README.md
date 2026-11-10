# minecraft-voices

Shared voice packs for the talking NPCs on the family Minecraft server (Paper 26.2 + Geyser for the Bedrock tablet).
Every model with talking NPCs adds its clips here, and one pack per edition carries them all.

| Path | What |
|---|---|
| `packs/voices_java.zip` | Java resource pack. The server pushes it to players (`server.properties` → `resource-pack`, raw URL of this file, SHA-1 in `packs/SHA1.txt`) |
| `packs/voices_bedrock.mcpack` | The same sounds for Bedrock. Goes in `plugins/Geyser-Spigot/packs/`; Geyser sends it to Bedrock players (loaded at server start) |
| `audio/` | Every clip, mono Ogg Vorbis, loudness-normalised (-16 LUFS). `audio/<model>/voice/...` per model, `audio/npcvoice/laugh/<voice>/` shared laughs |
| `audio/durations.json` | Clip lengths in seconds (the datapacks use them so an NPC never talks over itself) |
| `voices.json` | Voice registry: ElevenLabs voice per voice slug, its laughs, and which model/role uses it |
| `tools/talklib.py` | The talking-NPC engine: generates the datapack functions (proximity trigger, intro once, per-player line cycling, laughs) |
| `tools/build_packs.py` | Rebuilds both packs from `audio/` |
| `tools/el-watch.ps1`, `tools/el-actions.ps1` | ElevenLabs job runner for Windows (reads `ELEVENLABS_API_KEY` from the environment; never stores it) |
| `tools/process.py` | mp3 → mono ogg, trim, normalise, measure |
| `models/<model>/` | Each model's characters, lines (with audio tags), placement and pack patch generator |

Sound names: Java `minecraft:<model>.voice.<...>`, Bedrock `<model>.voice.<...>`; laughs `npcvoice.laugh.<voice>.<n>`.
Laughs belong to a voice, not a model: a new model that reuses a voice reuses its laughs.

Adding a model: write `models/<model>/<model>_talk.py` (roles with a voice slug, lines, NPCs), generate the clips with
the runner, process them into `audio/<model>/voice/`, run `tools/build_packs.py`, update `voices.json`, commit, and
update `resource-pack-sha1` on the server.
