import asyncio
import subprocess

async def run_script(prompt, script_path):
    command = ["python", script_path, prompt]
    process = await asyncio.create_subprocess_exec(*command)
    await process.wait()
    print()


async def main():
    # List of prompts
    prompts = [
        "\"What is Python?\"",
        "\"Tell me about Javascript\"",
        "\"Do you think that using microservices is a good architecture pattern?\"",
        "\"What is the difference between a cell in plants and animals?\""
    ]

    # Script path
    script_path = "test_streaming.py"  # Replace with the actual path to your script

    # Create tasks to run the scripts concurrently
    tasks = [run_script(prompt, script_path) for prompt in prompts]
    print("START")
    await asyncio.gather(*tasks)
    print("END")

if __name__ == "__main__":
    # List of prompts
    asyncio.run(main())
