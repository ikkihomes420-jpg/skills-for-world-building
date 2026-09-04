---
name: ai-research-suite
description: Comprehensive AI research and engineering skill suite containing 98 preserved specialist skills plus evidence-first governance and structured investigation workflows. Use when planning, implementing, evaluating, optimizing, serving, observing, or writing about AI research and engineering; conducting multi-item deep research, empirical analysis, replication, or evidence-led synthesis; route to the relevant bundled specialist skill without replacing its instructions, and apply research governance for multi-hypothesis, replication, experiment, evidence-led, or conclusion-writing projects.
license: MIT
metadata:
  source: Orchestra Research AI-Research-SKILLs
  bundled-skills: 98
  preservation: Original skill directories and resources are retained under references/skills/
---

# AI Research Suite

Use this umbrella skill as a router and a complete local knowledge bundle for AI research and engineering. **Do not summarize away, rewrite, or substitute the specialist instructions.** Select the narrowest relevant specialist skill, read its complete `SKILL.md`, and then read the referenced files inside that specialist directory as needed.

## Routing Protocol

1. Classify the request by task type and technical domain.
2. Select one primary specialist skill from the catalog below; select additional specialists when the task spans domains.
3. Read `references/skills/<skill-name>/SKILL.md` in full before acting.
4. Follow that skill’s workflows, scripts, references, and output requirements exactly. Treat the bundled skill as authoritative for its domain.
5. For cross-domain work, preserve each specialist’s constraints and reconcile them explicitly rather than flattening them into a generic procedure.
6. Report which specialist skill or skills were used when delivering results.
7. For multi-session, multi-hypothesis, replication, experiment-heavy, evidence-led, or conclusion-writing work, also apply the **Research Governance Layer** below. It coordinates project memory and rigor; it never overrides the selected specialist’s technical instructions.

## Structured Investigation and Empirical Research

Use this workflow for a comparison, landscape, survey, due-diligence study, literature review, empirical project, replication, or research report. Read `references/research-intake-and-empirical-workflow.md` before starting a multi-item investigation or empirical lifecycle. It defines the shared intake, evidence, batch-review, synthesis, and completion controls; it does not replace a selected specialist’s method-specific process.

| Request shape | Required action | Primary resource |
| --- | --- | --- |
| Bounded factual question | Research and cite sources proportionately; do not create unnecessary project artifacts. | Source notes. |
| Multi-item review or comparison | Define objects, fields, evidence/time boundaries, completion criteria, and human checkpoint; confirm before material-scale collection. | `templates/research-spec.yaml` |
| Empirical analysis, experiment, or replication | Establish governance artifacts and route to the narrowest technical specialist. | `references/research-governance/research-artifacts.md` |
| Research paper, report, or reusable artifact | Audit claims and limitations; route to relevant writing or ARA specialist after evidence review. | Claim–evidence ledger and selected specialist. |

For structured investigations, separate source extraction, analysis, and cross-source synthesis. Record required fields as sourced, unknown, or uncertain; never turn missing evidence into a confident value. Work in bounded batches, disclose blockers or source-quality concerns, and obtain a human checkpoint before a material scope, method, resource, or conclusion change. Validate the plan with `scripts/validate_research_spec.py <research-spec.yaml>` before claiming it is structurally complete. The validator checks record completeness, not factual accuracy or methodological quality.

For empirical research, apply the relevant lifecycle: question and design; evidence and literature; data and provenance; analysis and identification; writing and citation; reproducibility and release; review and response. Preserve assumptions, baselines, data transformations, diagnostics, robustness checks, environments, and regeneration paths. Use the complete reference for stage-specific directions and source provenance.

## Research Governance Layer

Use this layer **in addition to** the narrowest applicable specialist for any project with consequential evidence, more than one experiment, a need to distinguish confirmatory from exploratory work, or a planned research conclusion. Read `references/research-governance/research-artifacts.md` before establishing project records, protocols, evidence cards, claims, or a rigor audit. Use `scripts/validate_research_bundle.py` only with a local JSON bundle the user has provided or explicitly asked to create; inspect its report before claiming the record is complete.

Start with a research contract: an answerable question, target system/population, scope, decision consequence, primary evidence standard or metric, baseline, constraints, and an explicit human checkpoint for material changes in resources, safety, scope, or conclusion. A topic is not a research question until observations can meaningfully change the decision.

Maintain linked project artifacts: **research state**, **evidence cards**, **hypotheses**, **pre-execution protocols**, **experiment records**, **outer-loop syntheses**, and a **claim–evidence ledger**. Record sources, assumptions, limitations, environments, data/configuration versions, raw result locations, and negative or invalidated runs. Do not promote a pattern into a claim merely because it is convenient to narrate.

| Project action | Governance requirement | Technical work |
|---|---|---|
| Literature/bootstrap | Create evidence cards and identify gaps/limits. | Route to the domain specialist for source, data, or model context. |
| Hypothesis generation | State mechanism/rationale and a falsifiable prediction. | Use ideation specialists when appropriate. |
| Confirmatory experiment | Lock protocol, controls, primary metric, analysis plan, and stopping rule before outcome. | Follow the selected training/evaluation/analysis specialist. |
| Exploratory result | Label it exploratory and formulate a follow-up test if material. | Preserve raw artifacts and context. |
| Result batch or surprise | Run an outer-loop synthesis; deepen, broaden, pivot, pause, or conclude. | Return to literature or route to additional specialists as needed. |
| Report or paper | Audit every consequential claim for linked evidence, scope, and limitations. | Route to paper-writing, plotting, or presentation specialists. |

Use calibrated verbs. “Associated with,” “under the tested conditions,” and “in this implementation” often state evidence more accurately than “causes,” “generalizes,” or “proves.” Preserve the distinction between **confirmatory**, **exploratory**, **diagnostic**, and **replication** work. Failed execution is not a refuted hypothesis unless the failure was itself measured and diagnosed.

Run an outer loop after meaningful result batches, surprises, plateaus, contradictions, or material constraint changes. Synthesize patterns and limits, not just logs. Decide whether to deepen an effect, broaden the question, pivot assumptions, pause for a blocker, or conclude. Before conclusion, run the rigor rubric in the governance reference and check that every material claim links to evidence with appropriate scope, uncertainty, and reproducibility artifacts.

Do not imply that research will run indefinitely because a loop exists. Recurring or background work requires an approved cadence, inputs, stop condition, budget/resource boundary, review point, and delivery destination. Use the applicable automation guidance before configuring a recurring workflow.

## Specialist Catalog

### 00-autoresearch

| Skill | Use for | Source category |
| --- | --- | --- |
| `autoresearch` | Orchestrates end-to-end autonomous AI research projects using a two-loop architecture. The inner loop runs rapid experiment iterations with clear optimization targets. The outer loop synthesizes results, identifies patterns, and steers research direction. Routes to domain-specific skills for execution, supports continuous agent operation via Claude Code /loop and OpenClaw heartbeat, and produces research presentations and papers. Use when starting a research project, running autonomous experiments, or managing a multi-hypothesis research effort. | `0-autoresearch-skill` |

### 01-model-architecture

| Skill | Use for | Source category |
| --- | --- | --- |
| `distributed-llm-pretraining-torchtitan` | Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP). Use when pretraining Llama 3.1, DeepSeek V3, or custom models at scale from 8 to 512+ GPUs with Float8, torch.compile, and distributed checkpointing. | `01-model-architecture/torchtitan` |
| `implementing-llms-litgpt` | Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama, Gemma, Phi, Qwen, Mistral). Use when need clean model implementations, educational understanding of architectures, or production fine-tuning with LoRA/QLoRA. Single-file implementations, no abstraction layers. | `01-model-architecture/litgpt` |
| `mamba-architecture` | State-space model with O(n) complexity vs Transformers' O(n²). 5× faster inference, million-token sequences, no KV cache. Selective SSM with hardware-aware design. Mamba-1 (d_state=16) and Mamba-2 (d_state=128, multi-head). Models 130M-2.8B on HuggingFace. | `01-model-architecture/mamba` |
| `nanogpt` | Educational GPT implementation in ~300 lines. Reproduces GPT-2 (124M) on OpenWebText. Clean, hackable code for learning transformers. By Andrej Karpathy. Perfect for understanding GPT architecture from scratch. Train on Shakespeare (CPU) or OpenWebText (multi-GPU). | `01-model-architecture/nanogpt` |
| `rwkv-architecture` | RNN+Transformer hybrid with O(n) inference. Linear time, infinite context, no KV cache. Train like GPT (parallel), infer like RNN (sequential). Linux Foundation AI project. Production at Windows, Office, NeMo. RWKV-7 (March 2025). Models up to 14B parameters. | `01-model-architecture/rwkv` |

### 02-tokenization

| Skill | Use for | Source category |
| --- | --- | --- |
| `huggingface-tokenizers` | Fast tokenizers optimized for research and production. Rust-based implementation tokenizes 1GB in <20 seconds. Supports BPE, WordPiece, and Unigram algorithms. Train custom vocabularies, track alignments, handle padding/truncation. Integrates seamlessly with transformers. Use when you need high-performance tokenization or custom tokenizer training. | `02-tokenization/huggingface-tokenizers` |
| `sentencepiece` | Language-independent tokenizer treating text as raw Unicode. Supports BPE and Unigram algorithms. Fast (50k sentences/sec), lightweight (6MB memory), deterministic vocabulary. Used by T5, ALBERT, XLNet, mBART. Train on raw text without pre-tokenization. Use when you need multilingual support, CJK languages, or reproducible tokenization. | `02-tokenization/sentencepiece` |

### 03-fine-tuning

| Skill | Use for | Source category |
| --- | --- | --- |
| `axolotl` | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support | `03-fine-tuning/axolotl` |
| `llama-factory` | Expert guidance for fine-tuning LLMs with LLaMA-Factory - WebUI no-code, 100+ models, 2/3/4/5/6/8-bit QLoRA, multimodal support | `03-fine-tuning/llama-factory` |
| `peft-fine-tuning` | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when you need to train <1% of parameters with minimal accuracy loss, or for multi-adapter serving. HuggingFace's official library integrated with transformers ecosystem. | `03-fine-tuning/peft` |
| `unsloth` | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization | `03-fine-tuning/unsloth` |

### 04-mechanistic-interpretability

| Skill | Use for | Source category |
| --- | --- | --- |
| `nnsight-remote-interpretability` | Provides guidance for interpreting and manipulating neural network internals using nnsight with optional NDIF remote execution. Use when needing to run interpretability experiments on massive models (70B+) without local GPU resources, or when working with any PyTorch architecture. | `04-mechanistic-interpretability/nnsight` |
| `pyvene-interventions` | Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative intervention framework. Use when conducting causal tracing, activation patching, interchange intervention training, or testing causal hypotheses about model behavior. | `04-mechanistic-interpretability/pyvene` |
| `sparse-autoencoder-training` | Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable features. Use when discovering interpretable features, analyzing superposition, or studying monosemantic representations in language models. | `04-mechanistic-interpretability/saelens` |
| `transformer-lens-interpretability` | Provides guidance for mechanistic interpretability research using TransformerLens to inspect and manipulate transformer internals via HookPoints and activation caching. Use when reverse-engineering model algorithms, studying attention patterns, or performing activation patching experiments. | `04-mechanistic-interpretability/transformer-lens` |

### 05-data-processing

| Skill | Use for | Source category |
| --- | --- | --- |
| `nemo-curator` | GPU-accelerated data curation for LLM training. Supports text/image/video/audio. Features fuzzy deduplication (16× faster), quality filtering (30+ heuristics), semantic deduplication, PII redaction, NSFW detection. Scales across GPUs with RAPIDS. Use for preparing high-quality training datasets, cleaning web data, or deduplicating large corpora. | `05-data-processing/nemo-curator` |
| `ray-data` | Scalable data processing for ML workloads. Streaming execution across CPU/GPU, supports Parquet/CSV/JSON/images. Integrates with Ray Train, PyTorch, TensorFlow. Scales from single machine to 100s of nodes. Use for batch inference, data preprocessing, multi-modal data loading, or distributed ETL pipelines. | `05-data-processing/ray-data` |

### 06-post-training

| Skill | Use for | Source category |
| --- | --- | --- |
| `fine-tuning-with-trl` | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and reward model training. Use when need RLHF, align model with preferences, or train from human feedback. Works with HuggingFace Transformers. | `06-post-training/trl-fine-tuning` |
| `grpo-rl-training` | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training | `06-post-training/grpo-rl-training` |
| `miles-rl-training` | Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime. Use when training large MoE models with FP8/INT4, needing train-inference alignment, or requiring speculative RL for maximum throughput. | `06-post-training/miles` |
| `openrlhf-training` | High-performance RLHF framework with Ray+vLLM acceleration. Use for PPO, GRPO, RLOO, DPO training of large models (7B-70B+). Built on Ray, vLLM, ZeRO-3. 2× faster than DeepSpeedChat with distributed architecture and GPU resource sharing. | `06-post-training/openrlhf` |
| `simpo-training` | Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No reference model needed, more efficient than DPO. Use for preference alignment when want simpler, faster training than DPO/PPO. | `06-post-training/simpo` |
| `slime-rl-training` | Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. Use when training GLM models, implementing custom data generation workflows, or needing tight Megatron-LM integration for RL scaling. | `06-post-training/slime` |
| `torchforge-rl-training` | Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra from algorithms. Use when you want clean RL abstractions, easy algorithm experimentation, or scalable training with Monarch and TorchTitan. | `06-post-training/torchforge` |
| `verl-rl-training` | Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL). Use when implementing RLHF, GRPO, PPO, or other RL algorithms for LLM post-training at scale with flexible infrastructure backends. | `06-post-training/verl` |

### 07-safety-alignment

| Skill | Use for | Source category |
| --- | --- | --- |
| `constitutional-ai` | Anthropic's method for training harmless AI through self-improvement. Two-phase approach - supervised learning with self-critique/revision, then RLAIF (RL from AI Feedback). Use for safety alignment, reducing harmful outputs without human labels. Powers Claude's safety system. | `07-safety-alignment/constitutional-ai` |
| `llamaguard` | Meta's 7-8B specialized moderation model for LLM input/output filtering. 6 safety categories - violence/hate, sexual content, weapons, substances, self-harm, criminal planning. 94-95% accuracy. Deploy with vLLM, HuggingFace, Sagemaker. Integrates with NeMo Guardrails. | `07-safety-alignment/llamaguard` |
| `nemo-guardrails` | NVIDIA's runtime safety framework for LLM applications. Features jailbreak detection, input/output validation, fact-checking, hallucination detection, PII filtering, toxicity detection. Uses Colang 2.0 DSL for programmable rails. Production-ready, runs on T4 GPU. | `07-safety-alignment/nemo-guardrails` |
| `prompt-guard` | Meta's 86M prompt injection and jailbreak detector. Filters malicious prompts and third-party data for LLM apps. 99%+ TPR, <1% FPR. Fast (<2ms GPU). Multilingual (8 languages). Deploy with HuggingFace or batch processing for RAG security. | `07-safety-alignment/prompt-guard` |

### 08-distributed-training

| Skill | Use for | Source category |
| --- | --- | --- |
| `deepspeed` | Expert guidance for distributed training with DeepSpeed - ZeRO optimization stages, pipeline parallelism, FP16/BF16/FP8, 1-bit Adam, sparse attention | `08-distributed-training/deepspeed` |
| `huggingface-accelerate` | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic device placement, mixed precision (FP16/BF16/FP8). Interactive config, single launch command. HuggingFace ecosystem standard. | `08-distributed-training/accelerate` |
| `pytorch-fsdp2` | Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpointing. Use when models exceed single-GPU memory or when you need DTensor-based sharding with DeviceMesh. | `08-distributed-training/pytorch-fsdp2` |
| `pytorch-lightning` | High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerplate. Scales from laptop to supercomputer with same code. Use when you want clean training loops with built-in best practices. | `08-distributed-training/pytorch-lightning` |
| `ray-train` | Distributed training orchestration across clusters. Scales PyTorch/TensorFlow/HuggingFace from laptop to 1000s of nodes. Built-in hyperparameter tuning with Ray Tune, fault tolerance, elastic scaling. Use when training massive models across multiple machines or running distributed hyperparameter sweeps. | `08-distributed-training/ray-train` |
| `training-llms-megatron` | Trains large language models (2B-462B parameters) using NVIDIA Megatron-Core with advanced parallelism strategies. Use when training models >1B parameters, need maximum GPU efficiency (47% MFU on H100), or require tensor/pipeline/sequence/context/expert parallelism. Production-ready framework used for Nemotron, LLaMA, DeepSeek. | `08-distributed-training/megatron-core` |

### 09-infrastructure

| Skill | Use for | Source category |
| --- | --- | --- |
| `lambda-labs-gpu-cloud` | Reserved and on-demand GPU cloud instances for ML training and inference. Use when you need dedicated GPU instances with simple SSH access, persistent filesystems, or high-performance multi-node clusters for large-scale training. | `09-infrastructure/lambda-labs` |
| `modal-serverless-gpu` | Serverless GPU cloud platform for running ML workloads. Use when you need on-demand GPU access without infrastructure management, deploying ML models as APIs, or running batch jobs with automatic scaling. | `09-infrastructure/modal` |
| `skypilot-multi-cloud-orchestration` | Multi-cloud orchestration for ML workloads with automatic cost optimization. Use when you need to run training or batch jobs across multiple clouds, leverage spot instances with auto-recovery, or optimize GPU costs across providers. | `09-infrastructure/skypilot` |

### 10-optimization

| Skill | Use for | Source category |
| --- | --- | --- |
| `awq-quantization` | Activation-aware weight quantization for 4-bit LLM compression with 3x speedup and minimal accuracy loss. Use when deploying large models (7B-70B) on limited GPU memory, when you need faster inference than GPTQ with better accuracy preservation, or for instruction-tuned and multimodal models. MLSys 2024 Best Paper Award winner. | `10-optimization/awq` |
| `gguf-quantization` | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing flexible quantization from 2-8 bit without GPU requirements. | `10-optimization/gguf` |
| `gptq` | Post-training 4-bit quantization for LLMs with minimal accuracy loss. Use for deploying large models (70B, 405B) on consumer GPUs, when you need 4× memory reduction with <2% perplexity degradation, or for faster inference (3-4× speedup) vs FP16. Integrates with transformers and PEFT for QLoRA fine-tuning. | `10-optimization/gptq` |
| `hqq-quantization` | Half-Quadratic Quantization for LLMs without calibration data. Use when quantizing models to 4/3/2-bit precision without needing calibration datasets, for fast quantization workflows, or when deploying with vLLM or HuggingFace Transformers. | `10-optimization/hqq` |
| `ml-training-recipes` | Battle-tested PyTorch training recipes for all domains — LLMs, vision, diffusion, medical imaging, protein/drug discovery, spatial omics, genomics. Covers training loops, optimizer selection (AdamW, Muon), LR scheduling, mixed precision, debugging, and systematic experimentation. Use when training or fine-tuning neural networks, debugging loss spikes or OOM, choosing architectures, or optimizing GPU throughput. | `10-optimization/ml-training-recipes` |
| `optimizing-attention-flash` | Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long sequences (>512 tokens), encountering GPU memory issues with attention, or need faster inference. Supports PyTorch native SDPA, flash-attn library, H100 FP8, and sliding window attention. | `10-optimization/flash-attention` |
| `quantizing-models-bitsandbytes` | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memory is limited, need to fit larger models, or want faster inference. Supports INT8, NF4, FP4 formats, QLoRA training, and 8-bit optimizers. Works with HuggingFace Transformers. | `10-optimization/bitsandbytes` |

### 11-evaluation

| Skill | Use for | Source category |
| --- | --- | --- |
| `evaluating-code-models` | Evaluates code generation models across HumanEval, MBPP, MultiPL-E, and 15+ benchmarks with pass@k metrics. Use when benchmarking code models, comparing coding abilities, testing multi-language support, or measuring code generation quality. Industry standard from BigCode Project used by HuggingFace leaderboards. | `11-evaluation/bigcode-evaluation-harness` |
| `evaluating-llms-harness` | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs. | `11-evaluation/lm-evaluation-harness` |
| `nemo-evaluator-sdk` | Evaluates LLMs across 100+ benchmarks from 18+ harnesses (MMLU, HumanEval, GSM8K, safety, VLM) with multi-backend execution. Use when needing scalable evaluation on local Docker, Slurm HPC, or cloud platforms. NVIDIA's enterprise-grade platform with container-first architecture for reproducible benchmarking. | `11-evaluation/nemo-evaluator` |

### 12-inference-serving

| Skill | Use for | Source category |
| --- | --- | --- |
| `llama-cpp` | Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when CUDA is unavailable. Supports GGUF quantization (1.5-8 bit) for reduced memory and 4-10× speedup vs PyTorch on CPU. | `12-inference-serving/llama-cpp` |
| `serving-llms-vllm` | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory. Supports OpenAI-compatible endpoints, quantization (GPTQ/AWQ/FP8), and tensor parallelism. | `12-inference-serving/vllm` |
| `sglang` | Fast structured generation and serving for LLMs with RadixAttention prefix caching. Use for JSON/regex outputs, constrained decoding, agentic workflows with tool calls, or when you need 5× faster inference than vLLM with prefix sharing. Powers 300,000+ GPUs at xAI, AMD, NVIDIA, and LinkedIn. | `12-inference-serving/sglang` |
| `tensorrt-llm` | Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when you need 10-100x faster inference than PyTorch, or for serving models with quantization (FP8/INT4), in-flight batching, and multi-GPU scaling. | `12-inference-serving/tensorrt-llm` |

### 13-mlops

| Skill | Use for | Source category |
| --- | --- | --- |
| `experiment-tracking-swanlab` | Provides guidance for experiment tracking with SwanLab. Use when you need open-source run tracking, local or self-hosted dashboards, and lightweight media logging for ML workflows. | `13-mlops/swanlab` |
| `mlflow` | Track ML experiments, manage model registry with versioning, deploy models to production, and reproduce experiments with MLflow - framework-agnostic ML lifecycle platform | `13-mlops/mlflow` |
| `tensorboard` | Visualize training metrics, debug models with histograms, compare experiments, visualize model graphs, and profile performance with TensorBoard - Google's ML visualization toolkit | `13-mlops/tensorboard` |
| `weights-and-biases` | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B - collaborative MLOps platform | `13-mlops/weights-and-biases` |

### 14-agents

| Skill | Use for | Source category |
| --- | --- | --- |
| `autogpt-agents` | Autonomous AI agent platform for building and deploying continuous agents. Use when creating visual workflow agents, deploying persistent autonomous agents, or building complex multi-step AI automation systems. | `14-agents/autogpt` |
| `crewai-multi-agent` | Multi-agent orchestration framework for autonomous AI collaboration. Use when building teams of specialized agents working together on complex tasks, when you need role-based agent collaboration with memory, or for production workflows requiring sequential/hierarchical execution. Built without LangChain dependencies for lean, fast execution. | `14-agents/crewai` |
| `evolving-ai-agents` | Provides guidance for automatically evolving and optimizing AI agents across any domain using LLM-driven evolution algorithms. Use when building self-improving agents, optimizing agent prompts and skills against benchmarks, or implementing automated agent evaluation loops. | `14-agents/a-evolve` |
| `langchain` | Framework for building LLM-powered applications with agents, chains, and RAG. Supports multiple providers (OpenAI, Anthropic, Google), 500+ integrations, ReAct agents, tool calling, memory management, and vector store retrieval. Use for building chatbots, question-answering systems, autonomous agents, or RAG applications. Best for rapid prototyping and production deployments. | `14-agents/langchain` |
| `llamaindex` | Data framework for building LLM applications with RAG. Specializes in document ingestion (300+ connectors), indexing, and querying. Features vector indices, query engines, agents, and multi-modal support. Use for document Q&A, chatbots, knowledge retrieval, or building RAG pipelines. Best for data-centric LLM applications. | `14-agents/llamaindex` |

### 15-rag

| Skill | Use for | Source category |
| --- | --- | --- |
| `chroma` | Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-function API. Scales from notebooks to production clusters. Use for semantic search, RAG applications, or document retrieval. Best for local development and open-source projects. | `15-rag/chroma` |
| `faiss` | Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index types (Flat, IVF, HNSW). Use for fast k-NN search, large-scale vector retrieval, or when you need pure similarity search without metadata. Best for high-performance applications. | `15-rag/faiss` |
| `pinecone` | Managed vector database for production AI applications. Fully managed, auto-scaling, with hybrid search (dense + sparse), metadata filtering, and namespaces. Low latency (<100ms p95). Use for production RAG, recommendation systems, or semantic search at scale. Best for serverless, managed infrastructure. | `15-rag/pinecone` |
| `qdrant-vector-search` | High-performance vector similarity search engine for RAG and semantic search. Use when building production RAG systems requiring fast nearest neighbor search, hybrid search with filtering, or scalable vector storage with Rust-powered performance. | `15-rag/qdrant` |
| `sentence-transformers` | Framework for state-of-the-art sentence, text, and image embeddings. Provides 5000+ pre-trained models for semantic similarity, clustering, and retrieval. Supports multilingual, domain-specific, and multimodal models. Use for generating embeddings for RAG, semantic search, or similarity tasks. Best for production embedding generation. | `15-rag/sentence-transformers` |

### 16-prompt-engineering

| Skill | Use for | Source category |
| --- | --- | --- |
| `dspy` | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP's framework for systematic LM programming | `16-prompt-engineering/dspy` |
| `guidance` | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance - Microsoft Research's constrained generation framework | `16-prompt-engineering/guidance` |
| `instructor` | Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and stream partial results with Instructor - battle-tested structured output library | `16-prompt-engineering/instructor` |
| `outlines` | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and maximize inference speed with Outlines - dottxt.ai's structured generation library | `16-prompt-engineering/outlines` |

### 17-observability

| Skill | Use for | Source category |
| --- | --- | --- |
| `langsmith-observability` | LLM observability platform for tracing, evaluation, and monitoring. Use when debugging LLM applications, evaluating model outputs against datasets, monitoring production systems, or building systematic testing pipelines for AI applications. | `17-observability/langsmith` |
| `phoenix-observability` | Open-source AI observability platform for LLM tracing, evaluation, and monitoring. Use when debugging LLM applications with detailed traces, running evaluations on datasets, or monitoring production AI systems with real-time insights. | `17-observability/phoenix` |

### 18-multimodal

| Skill | Use for | Source category |
| --- | --- | --- |
| `audiocraft-audio-generation` | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text descriptions, create sound effects, or perform melody-conditioned music generation. | `18-multimodal/audiocraft` |
| `blip-2-vision-language` | Vision-language pre-training framework bridging frozen image encoders and LLMs. Use when you need image captioning, visual question answering, image-text retrieval, or multimodal chat with state-of-the-art zero-shot performance. | `18-multimodal/blip-2` |
| `clip` | OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. Use for image search, content moderation, or vision-language tasks without fine-tuning. Best for general-purpose image understanding. | `18-multimodal/clip` |
| `evaluating-cosmos-policy` | Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments. Use when setting up cosmos-policy for robot manipulation evaluation, running headless GPU evaluations with EGL rendering, or profiling inference latency on cluster or local GPU machines. | `18-multimodal/cosmos-policy` |
| `fine-tuning-openvla-oft` | Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot action generation with continuous action heads, LoRA adaptation, and FiLM conditioning on LIBERO simulation and ALOHA real-world setups. Use when reproducing OpenVLA-OFT paper results, training custom VLA action heads (L1 or diffusion), deploying server-client inference for ALOHA, or debugging normalization, LoRA merge, and cross-GPU issues. | `18-multimodal/openvla-oft` |
| `fine-tuning-serving-openpi` | Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast, pi0.5) using JAX or PyTorch backends for robot policy inference across ALOHA, DROID, and LIBERO environments. Use when adapting pi0 models to custom datasets, converting JAX checkpoints to PyTorch, running policy inference servers, or debugging norm stats and GPU memory issues. | `18-multimodal/openpi` |
| `llava` | Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA language models. Supports multi-turn image chat, visual question answering, and instruction following. Use for vision-language chatbots or image understanding tasks. Best for conversational image analysis. | `18-multimodal/llava` |
| `segment-anything-model` | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as prompts, or automatically generate all object masks in an image. | `18-multimodal/segment-anything` |
| `stable-diffusion-image-generation` | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, performing image-to-image translation, inpainting, or building custom diffusion pipelines. | `18-multimodal/stable-diffusion` |
| `whisper` | OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR. | `18-multimodal/whisper` |

### 19-emerging-techniques

| Skill | Use for | Source category |
| --- | --- | --- |
| `knowledge-distillation` | Compress large language models using knowledge distillation from teacher to student models. Use when deploying smaller models with retained performance, transferring GPT-4 capabilities to open-source models, or reducing inference costs. Covers temperature scaling, soft targets, reverse KLD, logit distillation, and MiniLLM training strategies. | `19-emerging-techniques/knowledge-distillation` |
| `long-context` | Extend context windows of transformer models using RoPE, YaRN, ALiBi, and position interpolation techniques. Use when processing long documents (32k-128k+ tokens), extending pre-trained models beyond original context limits, or implementing efficient positional encodings. Covers rotary embeddings, attention biases, interpolation methods, and extrapolation strategies for LLMs. | `19-emerging-techniques/long-context` |
| `model-merging` | Merge multiple fine-tuned models using mergekit to combine capabilities without retraining. Use when creating specialized models by blending domain-specific expertise (math + coding + chat), improving performance beyond single models, or experimenting rapidly with model variants. Covers SLERP, TIES-Merging, DARE, Task Arithmetic, linear merging, and production deployment strategies. | `19-emerging-techniques/model-merging` |
| `model-pruning` | Reduce LLM size and accelerate inference using pruning techniques like Wanda and SparseGPT. Use when compressing models without retraining, achieving 50% sparsity with minimal accuracy loss, or enabling faster inference on hardware accelerators. Covers unstructured pruning, structured pruning, N:M sparsity, magnitude pruning, and one-shot methods. | `19-emerging-techniques/model-pruning` |
| `moe-training` | Train Mixture of Experts (MoE) models using DeepSpeed or HuggingFace. Use when training large-scale models with limited compute (5× cost reduction vs dense models), implementing sparse architectures like Mixtral 8x7B or DeepSeek-V3, or scaling model capacity without proportional compute increase. Covers MoE architectures, routing mechanisms, load balancing, expert parallelism, and inference optimization. | `19-emerging-techniques/moe-training` |
| `speculative-decoding` | Accelerate LLM inference using speculative decoding, Medusa multiple heads, and lookahead decoding techniques. Use when optimizing inference speed (1.5-3.6× speedup), reducing latency for real-time applications, or deploying models with limited compute. Covers draft models, tree-based attention, Jacobi iteration, parallel token generation, and production deployment strategies. | `19-emerging-techniques/speculative-decoding` |

### 20-ml-paper-writing

| Skill | Use for | Source category |
| --- | --- | --- |
| `academic-plotting` | Generates publication-quality figures for ML papers from research context. Given a paper section or description, extracts system components and relationships to generate architecture diagrams via Gemini. Given experiment results or data, auto-selects chart type and generates data-driven figures via matplotlib/seaborn. Use when creating any figure for a conference paper. | `20-ml-paper-writing/academic-plotting` |
| `ml-paper-writing` | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, verifying citations, or preparing camera-ready submissions. For systems venues (OSDI, NSDI, ASPLOS, SOSP), use systems-paper-writing instead. | `20-ml-paper-writing/ml-paper-writing` |
| `presenting-conference-talks` | Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script. Use when preparing oral talks, spotlight presentations, or invited talks for ML and systems conferences. | `20-ml-paper-writing/presenting-conference-talks` |
| `systems-paper-writing` | Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys. Provides paragraph-level structural blueprints, writing patterns, venue-specific checklists, reviewer guidelines, LaTeX templates, and conference deadlines. Use this skill for all systems conference paper writing. | `20-ml-paper-writing/systems-paper-writing` |

### 21-research-ideation

| Skill | Use for | Source category |
| --- | --- | --- |
| `brainstorming-research-ideas` | Guides researchers through structured ideation frameworks to discover high-impact research directions. Use when exploring new problem spaces, pivoting between projects, or seeking novel angles on existing work. | `21-research-ideation/brainstorming-research-ideas` |
| `creative-thinking-for-research` | Applies cognitive science frameworks for creative thinking to CS and AI research ideation. Use when seeking genuinely novel research directions by leveraging combinatorial creativity, analogical reasoning, constraint manipulation, and other empirically grounded creative strategies. | `21-research-ideation/creative-thinking-for-research` |

### 22-agent-native-research-artifact

| Skill | Use for | Source category |
| --- | --- | --- |
| `ara-compiler` | Compiles any research input — PDF papers, GitHub repositories, experiment logs, code directories, or raw notes — into a complete Agent-Native Research Artifact (ARA) with cognitive layer (claims, concepts, heuristics), physical layer (configs, code stubs), exploration graph, and grounded evidence. Use when ingesting a paper or codebase into a structured, machine-executable knowledge package, building an ARA from scratch, or converting research outputs into a falsifiable, agent-traversable form. | `22-agent-native-research-artifact/compiler` |
| `ara-research-manager` | Records research provenance as a post-task epilogue, scanning conversation history at the end of a coding or research session to extract decisions, experiments, dead ends, claims, heuristics, and pivots, and writing them into the ara/ directory with user-vs-AI provenance tags. Use as a session epilogue — never during execution — to maintain a faithful, auditable trace of how a research project actually evolved. | `22-agent-native-research-artifact/research-manager` |
| `ara-rigor-reviewer` | Performs ARA Seal Level 2 semantic epistemic review on Agent-Native Research Artifacts, scoring six dimensions (evidence relevance, falsifiability, scope calibration, argument coherence, exploration integrity, methodological rigor) and producing a constructive, severity-ranked report with a Strong Accept-to-Reject recommendation. Use after Level 1 structural validation passes, when an ARA needs an objective epistemic critique before publication or release. | `22-agent-native-research-artifact/rigor-reviewer` |

## Preservation and Scope

The complete original skill packages are retained below `references/skills/`, including each original `SKILL.md`, reference documents, scripts, templates, and other bundled resources. The umbrella file adds routing; it does not replace the specialist content. The local structured-investigation reference and research-spec validator are independently written integrations informed by the provenance noted in `references/research-intake-and-empirical-workflow.md`; they do not import or execute external repository code. If a specialist skill contains its own dependency, safety, citation, or tool-use requirements, retain and obey them when that specialist is selected.

## Bundle Layout

```text
ai-research-suite/
├── SKILL.md
├── scripts/
│   ├── validate_research_bundle.py
│   └── validate_research_spec.py
├── templates/
│   └── research-spec.yaml
└── references/
    ├── research-governance/
    ├── research-intake-and-empirical-workflow.md
    └── skills/
        ├── <specialist-skill-1>/
        ├── <specialist-skill-2>/
        └── ... 98 preserved specialist skill directories
```
