# ch07 context7 current docs

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
Use the Context7 MCP server to check current documentation for Spring AI MCP
server support.

Resolve the relevant Spring AI documentation/library entry first. Then summarize
what the current docs say about exposing tools, MCP server setup, transports,
and any version/setup caveats that would matter to a project like MockHub.

Keep this concise. Do not edit files.
```

Output:

```text
## Spring AI MCP Server — Current Docs Summary

**Library used:** `/websites/spring_io_spring-ai_reference` (docs.spring.io/spring-ai/reference, High reputation).

### Starter dependencies (pick one per transport)
| Transport | Starter |
|---|---|
| STDIO | `spring-ai-starter-mcp-server` |
| SSE / Streamable-HTTP / Stateless (servlet) | `spring-ai-starter-mcp-server-webmvc` |
| SSE / Streamable-HTTP / Stateless (reactive) | `spring-ai-starter-mcp-server-webflux` |
| Streamable HTTP only | `spring-ai-starter-mcp-server-streamable-webmvc` |

Transport is then chosen via `spring.ai.mcp.server.protocol` = `STDIO` | `SSE` | `STREAMABLE`.

### Minimal YAML
```yaml
spring:
  ai:
    mcp:
      server:
        name: mockhub-mcp
        version: 1.0.0
        type: SYNC            # or ASYNC
        protocol: STREAMABLE  # or SSE / STDIO
        capabilities:
          tool: true
          resource: true
          prompt: true
          completion: true
        streamable-http:
          mcp-endpoint: /api/mcp
          keep-alive-interval: 30s
```

### Exposing tools (the part that matters for MockHub)
Two flavors, both documented as current:

1. **`@Tool` on service methods + `MethodToolCallbackProvider` bean** — the recommended path:
   ```java
   @Service
   class WeatherService {
       @Tool(description = "Get weather by city")
       public String getWeather(@ToolParam(description="city") String city) { ... }
   }

   @Bean
   ToolCallbackProvider weatherTools(WeatherService s) {
       return MethodToolCallbackProvider.builder().toolObjects(s).build();
   }
   ```
2. **Custom `ToolCallbackProvider` bean** built from an arbitrary `List<ToolCallback>` via `ToolCallbackProvider.from(tools)` — for dynamically-built tools.

Any bean of type `ToolCallbackProvider` is auto-registered with the MCP server — no extra wiring.

`★ Insight ─────────────────────────────────────`
- The same `@Tool`/`@ToolParam` annotations work for both in-process `ChatClient.tools(...)` calls and remote MCP exposure. That means for MockHub, you can keep one annotated service and decide per-deployment whether it's called locally or over MCP.
- `MethodToolCallbackProvider` reflects over the bean's methods, so adding a new tool is literally "add an `@Tool` method" — no registry to touch.
- Protocol vs. starter is decoupled: pick the starter (servlet vs. reactive vs. STDIO-only) and then choose `protocol:` inside it. Picking the wrong starter (e.g., reactive on a webmvc app) is the usual setup trap.
`─────────────────────────────────────────────────`

### Caveats worth noting for MockHub
- **Versioning:** docs list Spring AI versions through `1.1.x` and `2.0.0-mX`. MCP server APIs went through several rounds in the 1.0 → 1.1 milestones; pin a version explicitly in `pom.xml` rather than relying on BOMs from older guides.
- **Sync vs. async** is set by `spring.ai.mcp.server.type` and must match your starter (reactive starter → `ASYNC`).
- **Change notifications** (`tool-change-notification`, `resource-change-notification`, `prompt-change-notification`) only meaningfully fire on SSE/Streamable transports, not STDIO.
- **Endpoint path** defaults differ per transport; Streamable HTTP uses `streamable-http.mcp-endpoint` (example shows `/api/mcp`). Make it explicit so the MockHub client config is unambiguous.
- The **stateless** variant (`mcp-stateless-server-boot-starter`) is the right pick if MockHub will run behind a load balancer with no session affinity — it's the example used in the docs for `MethodToolCallbackProvider`.

No files changed.
```
