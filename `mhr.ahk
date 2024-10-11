; Utility Configs
    #NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
    #SingleInstance force
    global PREVIOUS_MODIfIED
    FileGetTime PREVIOUS_MODIfIED, %A_ScriptFullPath%
    SetTimer CheckScriptUpdate, 100, 0x7FFFFFFF ; Auto Reload If ModIfied, 100 ms, highest priority
    SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.


; Script Configs
    SetKeyDelay, 80, 70
    SetTitleMatchMode 3
    global WindowTitle := "Monster Hunter Rise"


; KeyBind
    F9::Cancel()
    F10::Apply()
    F12::Reload


; Script Methods
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


; Utility Methods
    ClickIfActive(keyName, sendCount=1, autoExit=True)
    {
        While(sendCount > 0)
        {
            If WinActive(WindowTitle){
                MouseClick, %keyName%
                sendCount-=1
            }
            Else{
                If autoExit{
                    Exit
                }
            }
            Sleep, 1
        }
    }

    SendIfActive(keyName, sendCount=1, autoExit=True)
    {
        While(sendCount > 0)
        {
            If WinActive(WindowTitle){
                Send, {%keyName%}
                sendCount-=1
            }
            Else{
                If autoExit{
                    Exit
                }
            }
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

; Script End