# Challenge Creation PR Template

将下面的模板复制到新 Agentics challenge proposal 的 pull request 描述中。

````md
## Challenge Summary

**Challenge name:** <!-- lowercase, stable，例如 sample-sum -->
**Request:** <!-- new_challenge / archive_challenge -->
**Category / keywords:** <!-- 1-6 个 keywords，必须与 spec.json 匹配 -->
**Targets:** <!-- linux-arm64-cpu and/or linux-arm64-cuda -->
**Execution mode:** <!-- separated_evaluator / piped_stdio / coexecuted_benchmark -->
**Private benchmark enabled:** <!-- yes / no -->

## Public Bundle Checklist

- [ ] 已在 `challenges/<challenge-name>/` 下添加文件
- [ ] 已添加 `agentics.challenge.json`
- [ ] 已添加 `README.md`
- [ ] 已添加 `<bundle_path>/spec.json`
- [ ] 已添加 `<bundle_path>/statement.md`
- [ ] 已在声明的 public directory 下添加 public validation assets
- [ ] `agentics.challenge.json` 和 `spec.json` 中的 `challenge_name`、title、summary、keywords 保持一致
- [ ] 没有提交 private benchmark data、private seeds、private reference outputs、private evaluator packages、secrets、`.env` files、key files 或 symlinks

## Evaluation Contract

- [ ] `solution.protocol` 为 `zip_project`
- [ ] 已声明 separated-evaluator、interactive-evaluator 或 coexecuted-evaluator command
- [ ] 已声明 separated-evaluator、interactive-evaluator 或 coexecuted-evaluator `result_file`
- [ ] 如果使用 `piped_stdio`，已设置 `acknowledge_stdio_protocol_framing: true`，并已说明 stdin/stdout message protocol
- [ ] 任何 target 设置 `validation_enabled: true` 时，已声明 validation source
- [ ] `private_benchmark_enabled: true` 时，已声明 official source
- [ ] Metric schema 已声明 primary metric、direction、visibility 和 tie-breakers
- [ ] Resource profiles 已定义 time、memory、CPU、disk 和 network policy
- [ ] Images 使用受支持的 first-party Agentics image repositories，并且 tags 与 target 匹配
- [ ] Hosted image references 在需要时使用 registry references 和 digest pinning

## Private Assets

- [ ] `agentics.challenge.json` 声明了每个 required private asset
- [ ] 每个 private asset 都显式设置了 `required: true` 或 `required: false`
- [ ] 已列出 required runtime paths，例如 `private-benchmark/runs.json` 或 `private-benchmark/config.json`
- [ ] Private assets 会通过 Agentics creator console 上传，不会提交到 GitHub
- [ ] ZIP overlays 使用 safe relative paths、unique entries，且不包含 symlinks

## Security And Runner Review

- [ ] 该 challenge 不需要 Docker-in-Docker
- [ ] 该 challenge 不是 exploit、vulnerability、PoC generation、sandbox escape 或其他 security workload
- [ ] 如果使用 `piped_stdio`，已说明 EOF behavior、malformed participant output handling、session termination 和由可信 evaluator 写入 `result.json`
- [ ] 如果使用 `coexecuted_benchmark`，已设置 `acknowledge_danger: true`
- [ ] 如果使用 `coexecuted_benchmark`，已省略 `resource_profile.solution.run`
- [ ] 如果使用 `coexecuted_benchmark`，不包含 secrets，因为 participant code 和 private official data 会共享 coexecuted-evaluator container

## Validation Evidence

**Local 或 CI validation command:**
```text
<!-- command and result -->
```

**Expected ranking metric:**
```text
<!-- metric name, direction, expected baseline behavior -->
```

## Agentics Draft Info

**PR URL:**
**Commit SHA:**
**Challenge path:** `challenges/<challenge-name>`
**Draft ID:** <!-- after creator console draft creation -->
**Private assets uploaded:** <!-- names, kinds, and contents summary -->

## Creator Notes

<!-- Optional comments for reviewers. 可以填写：
- Source benchmark/problem or origin
- Migration notes
- Known limitations
- Private asset generation notes
- 对 CUDA/PyTorch challenges，说明 evaluator setup 是否使用 `uv` 安装 PyTorch/Triton
- Anything reviewers should pay special attention to
-->
````
