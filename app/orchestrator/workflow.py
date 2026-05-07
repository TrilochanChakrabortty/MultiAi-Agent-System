from app.agents.planner import PlannerAgent
from app.agents.executor import TaskExecutorAgent
from app.services.db_service import DBService
from app.tools.tool_selector import ToolSelector
from app.core.logger import logger


class AgentOrchestrator:

    @staticmethod
    async def run(query: str, session_id: str):

        try:
            # -----------------------------
            # STEP 1: FETCH SESSION MEMORY
            # -----------------------------
            history = DBService.get_session_history(session_id)
            context_history = "\n".join(history[-3:])  # last 3 queries

            # -----------------------------
            # STEP 2: SAVE CURRENT QUERY
            # -----------------------------
            query_id = DBService.save_query(session_id, query)

            # -----------------------------
            # STEP 3: TOOL DECISION
            # -----------------------------
            tool = await ToolSelector.select_tool(query)
            logger.info(f"[Orchestrator] Tool Selected: {tool}")

            # -----------------------------
            # STEP 4: TASK GENERATION
            # -----------------------------
            if "rag" in tool:
                # 🔥 IMPORTANT: No task splitting for RAG
                tasks = [query]
            else:
                tasks = await PlannerAgent.create_plan(query)

            results = []

            # -----------------------------
            # STEP 5: EXECUTION LOOP
            # -----------------------------
            for task in tasks:

                task_id = DBService.save_task(query_id, task)

                # Inject memory into task
                enhanced_task = f"""
                Previous context:
                {context_history}

                Current task:
                {task}
                """

                result = await TaskExecutorAgent.execute(enhanced_task, session_id)

                DBService.save_result(task_id, str(result))
                
                results.append({
                    "task": task,
                    "answer": result.get("answer"),
                    "sources": result.get("sources"),
                    "tool_used": result.get("tool_used"),
                    "reason": result.get("reason"),
                    "steps": result.get("steps")
                })

            # -----------------------------
            # STEP 6: FINAL RESPONSE
            # -----------------------------
            return {
                "query": query,
                "session_id": session_id,
                "results": results
            }

        except Exception as e:
            logger.error(f"[Orchestrator Error]: {str(e)}")

            return {
                "query": query,
                "results": ["System error occurred"]
            }