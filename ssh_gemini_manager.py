# File Name: ssh_gemini_manager.py
# This module handles Gemini AI integration and SSH execution.

import google.generativeai as genai
import paramiko

def configure_gemini(api_key):
    """Configures the Gemini API."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        return f"Error configuring Gemini: {e}"

def get_linux_command_from_gemini(model, prompt):
    """
    Converts a natural language prompt into a single Linux command using Gemini.
    """
    try:
        # We create a very specific prompt for the AI to ensure it returns only a command
        full_prompt = (
            "You are an expert Linux system administrator. Your task is to convert the user's "
            "request into a single, safe, and executable Linux command. "
            "Do not provide any explanation, quotes, or formatting. Only output the raw command.\n"
            f"User Request: '{prompt}'\n"
            "Generated Command:"
        )
        response = model.generate_content(full_prompt)
        # Clean up the response to get only the command
        command = response.text.strip().replace('`', '')
        return command
    except Exception as e:
        return f"Error generating command: {e}"

def execute_remote_command(host, port, username, password, command):
    """
    Connects to a remote server via SSH and executes a given command.
    Returns the command's output or an error message.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        # Return output if available, otherwise the error
        return output if output else error
            
    except paramiko.AuthenticationException:
        return "SSH Authentication Error: Please check your username and password in my_secrets.py."
    except Exception as e:
        return f"An unexpected SSH error occurred: {e}"
    finally:
        ssh.close()
