document.addEventListener("DOMContentLoaded", () => {
  // Function to generate modals
  function createModals() {
    const modalsHTML = `
        <!-- Login Modal -->
        <div id="login-modal" class="modal">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-body">
                <div class="log-in-box">
                  <form id="login-form" class="login-form-fix">
                    <div>
                      <h3>Welcome back</h3>
                    </div>
                    <input type="text" id="login-username" placeholder="Username" class="input" required="">
                    <input type="password" id="login-password" placeholder="Password" class="input" required="">
                    <a href="/forgot-password">Forgot Password?</a>
                    <button type="submit" class="btn">Log In</button>
                    <svg width="158" height="93" viewBox="0 0 158 93" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <g filter="url(#filter0_f_480_3)">
                        <rect x="29" y="29" width="100" height="35" rx="17.5" fill="#154F48" />
                      </g>
                      <defs>
                        <filter id="filter0_f_480_3" x="0" y="0" width="158" height="93" filterUnits="userSpaceOnUse"
                          color-interpolation-filters="sRGB">
                          <feFlood flood-opacity="0" result="BackgroundImageFix" />
                          <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape" />
                          <feGaussianBlur stdDeviation="14.5" result="effect1_foregroundBlur_480_3" />
                        </filter>
                      </defs>
                    </svg>
                    <div id="login-message" class="message"></div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Signup Modal -->
        <div id="signup-modal" class="modal">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-body">
                <div class="sign-up-box">
                  <form id="signup-form">
                    <div>
                      <h3>Create an account</h3>
                    </div>
                    <div class="inputs">
                      <input type="text" id="username" name="username" placeholder="Username" class="input" required />
                      <input type="email" id="email" name="email" placeholder="Email" class="input" required />
                      <input type="password" id="password" name="password" placeholder="Password" class="input" required />
                      <input type="password" id="verify-password" name="verify_password" placeholder="Verify Password"
                        class="input" required />
                    </div>
                    <button type="submit" class="btn">Sign Up</button>
                    <div id="signup-message" class="message"></div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    document.body.insertAdjacentHTML("beforeend", modalsHTML);
  }

  // Toggle modal visibility with modal ID
  function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal.classList.contains("visible")) {
      closeModal(modalId);
    } else {
      showModal(modalId);
    }
  }

  // Show modal
  function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add("visible");
  }

  // Close modal
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove("visible");
  }

  // Close modal when clicking outside of the modal dialog
  function attachOutsideClickHandlers() {
    document.querySelectorAll(".modal").forEach((modal) => {
      modal.addEventListener("click", function (event) {
        if (!event.target.closest(".modal-dialog")) {
          closeModal(modal.id);
        }
      });
    });
  }

  // Initialize modals
  createModals();
  attachOutsideClickHandlers();

  // Expose toggle functions globally if needed
  window.toggleModal = toggleModal;
  window.showModal = showModal;
  window.closeModal = closeModal;
});
