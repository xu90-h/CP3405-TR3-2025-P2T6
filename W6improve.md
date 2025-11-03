<img width="1867" height="1059" alt="스크린샷 2025-11-03 13 01 22" src="https://github.com/user-attachments/assets/52f91b16-9870-470c-a718-19543f26e9f2" />#  SmartSeat Code Improvement Presentation

## Role Update
Originally, my role was **AI/ML**,  
but it has now been **changed to Developer** to focus more on front-end improvements, code refactoring, and usability enhancements for the SmartSeat project.

---

## Improvement 1 — Toast Notifications (UX)
**Before:**  
- Used blocking `alert()` pop-ups that interrupted the user flow.  

**After:**  
- Replaced with **non-blocking toast messages** for smoother feedback.  
- Users can now see multiple messages stacked without interruptions.  

###  Demo

<img width="497" height="1036" alt="스크린샷 2025-11-03 13 10 23" src="https://github.com/user-attachments/assets/483d48e3-492e-422f-ada5-a69720279250" />


*Result:*  

<img width="1867" height="1059" alt="스크린샷 2025-11-03 13 01 22" src="https://github.com/user-attachments/assets/b3f41cd0-5d03-4351-95c1-3468fa8f759c" />

Clear, instant feedback — users don’t have to close pop-ups manually, improving flow and usability.



---

## Improvement 2 — Keyboard & Screen Reader Accessibility
**Before:**  
- Seat selection worked only with a mouse.  

**After:**  
- Added `role="button"`, `tabindex`, and `aria-label` for screen readers.  
- Seats can now be selected using **Enter** or **Space** keys.

###  Code Snippet

<img width="778" height="131" alt="스크린샷 2025-11-03 13 02 28" src="https://github.com/user-attachments/assets/d4cf672d-9eb3-4677-ba29-3649044d7c4b" />

 *Result:*  
Visually impaired users and keyboard-only users can navigate and interact with seats easily.

##  Next Week’s Plan
- Collaborate with team members to **separate the merged HTML code** into modular, maintainable files.  
  (Currently, all HTML, CSS, and JS are combined into a single file.)  
- Continue improving **readability, reusability**, and **structure** for easier updates and teamwork.  
- Prepare a short demo showing the separated version and folder structure.

