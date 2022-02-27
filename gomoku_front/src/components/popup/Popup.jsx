import React from "react";

export function Popup(props) {
  return (
    <div
      id="popup"
      className={props.popup !== false ? "popup popup--visible" : "popup"}
    >
      <div className="popup__content">
        {props.children}
        {props.hidePopup && (
          <div onClick={() => props.hidePopup(false)} className="popup__close">
            x
          </div>
        )}
      </div>
    </div>
  );
}
