CHANGELOG
---

**Patch 0.4**

_Release Date: 1 Nov 2017_ [unreleased]

* UI
    * Added `Ctrl+Q` shortcut to easily quit the timer without navigating into the notification area

* Codebase
    * Python upgraded from 3.5.2 to **3.6.3**
    * PyQt upgraded from 5.8.1 to **5.9.1**

* Things to implement
    * Consolidate settings into a Settings dialog

* Taking into consideration
    * Possible revamping the GUI design using Qt Style Sheet
    * Auto-hide feature

* Issue(s) in the previous version
    * Timer slows down when the size of the LCD display increases
    * Restrict the user on entering existing hotkeys to eliminate hotkey conflict 


**Patch 0.3**

_Release Date: 1 Jul 2017_

* Highlights
    * User can now set his/her preferred shortcuts keys to control the timer.
    * Tenny is now accessible and controllable in the notification area.
    * Window opacity is now adjustable.

* Behavior 
    * Tenny will still run in the background if the window is closed. It can only be close in the notification area. 

* User Interface (UI)
    * Last known position and size of the window is now retrieved upon re-opening the app.


**Patch 0.2**

_Release Date: 1 Jun 2017_

* Highlight
    * Added hotkey support.
    
* User Interface (UI)
    * Can now be resize.
    * Added stopwatch icon in the taskbar.
    * Added tooltip in the Start/Stop and Reset buttons.


**Patch 0.1**

_Release Date: 16 Mar 2017_

* Feature
    * With `START`, `STOP` and `RESET` button to control the timer.
    * Semi-transparent and fixed window size.
    * Always on top.
    
    