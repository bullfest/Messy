(ns messy.views
  (:require
    [re-frame.core :as re-frame]
    [reagent.core :as reagent]
    [messy.events :as events]
    [messy.subs :as subs]
    ))


(defn username-form []
      (let [username (re-frame/subscribe [::subs/username])]
           [:div
            [:input {:name        "username"
                     :class       "form-control"
                     :type        "text"
                     :placeholder "Username"
                     :value       @username
                     :on-change   #(re-frame/dispatch [::events/set-username (-> % .-target .-value)])}]]))

(defn message-form []
      (let [sender (re-frame/subscribe [::subs/username])
            recipient (reagent/atom "")
            message (reagent/atom "")]
           [:form {:on-submit (fn [e]
                                  (.preventDefault e)
                                  (re-frame/dispatch [::events/create-message @message @recipient @sender])
                                  )}
            [:div {:class "form-group"}
             [:label {:for "recipient"} "Recipient"]
             [:input {:name      "recipient"
                      :class     "form-control"
                      :type      "text"
                      :on-change #((do
                                     (reset! recipient (-> % .-target .-value .toLowerCase))))

                      }]]
            [:div {:class "form-group"}
             [:label {:for "message"} "Message"]
             [:textarea {:name      "message"
                         :class     "form-control"
                         :on-change #((do
                                        (reset! message (-> % .-target .-value))))

                         }]]
            [:button {:class "btn btn-primary "} "Send"]
            ]))


(defn main-panel []
      [:div {:class "container mt-4"}
       [:div {:class "d-flex flex-row justify-content-between"}
        [:h1 "Welcome to Messy"]
        (username-form)]
       [:div {:class "container"}
        (message-form)]])