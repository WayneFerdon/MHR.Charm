; Recommended for performance and compatibility with future AutoHotkey releases.
#NoEnv

; Auto Reload If ModIfied
#SingleInstance force
global PREVIOUS_MODIfIED
FileGetTime PREVIOUS_MODIfIED, %A_ScriptFullPath%
SetTimer CheckScriptUpdate, 100, 0x7FFFFFFF ; 100 ms, highest priority

; Ensures a consistent starting directory.
SetWorkingDir %A_ScriptDir%

SetTitleMatchMode 3

SetKeyDelay, 80, 70
global WindowName := "Monster Hunter Rise"

F9::Cancel()
F10::Apply()
F12::Reload

Cancel()
{
    SendIfActive("Esc")
    Next(100)
}

Apply()
{
    SendIfActive("Enter")
    Next(3000)
}

; F9
Next(delay)
{
    SendIfActive("Right")
    SendIfActive("Enter")
    Sleep, %delay%
    SendIfActive("Enter")
    ; Sleep, 100
    SendIfActive("R")
    ; Sleep, 100
    SendIfActive("Enter")
    ; Sleep, 100
    SendIfActive("Enter")
}

ClickIfActive(keyName, sendCount=1)
{
    While(sendCount > 0)
    {
        If WinActive(WindowName)
            MouseClick, %keyName%
        Else
            Exit
        sendCount-=1
    }
}

SendIfActive(keyName, sendCount=1)
{
    While(sendCount > 0)
    {
        If WinActive(WindowName)
            Send, {%keyName%}
        Else
            Exit
        sendCount-=1
        Sleep, 1
    }
}

CheckScriptUpdate()
{
    FileGetTime curModTime, %A_ScriptFullPath%
    If (curModTime <> PREVIOUS_MODIfIED)
    {
        Loop
        {
            Reload
            Sleep 300 ; ms
            MsgBox 0x2, %A_ScriptName%, Reload failed. ; 0x2 = Abort/Retry/Ignore
            IfMsgBox Abort
            {
                ExitApp
            }
            IfMsgBox Ignore
            {
                Break
            }
        } ; loops reload on "Retry"
    }
} 