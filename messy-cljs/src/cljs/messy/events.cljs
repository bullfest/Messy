(ns messy.events
  (:require
    [re-frame.core :as re-frame]
    [day8.re-frame.http-fx]
    [ajax.core :as ajax]
    [clojure.string :as str]
    [messy.db :as db]
    [messy.config :as cfg]
    ))

(comment "--- DB management events ---")
(re-frame/reg-event-db
  ::initialize-db
  (fn [_ _]
      db/default-db))

(re-frame/reg-event-db
  ::set-username
  (fn [db [_ value]]
      (assoc db :username value)))

(re-frame/reg-event-db
  ::set-messages
  (fn [db [_ value]]
      (assoc db :messages value)))

(re-frame/reg-event-db
  ::remove-message
  (fn [db [_ message-id]]
      (assoc db :messages (filter #(not= (:id %)  message-id) (:messages db)))))

(comment "--- Helpers ---")
(defn filter-blank [map]
      (into {} (filter #(seq (second %)) map)))


(comment "--- Events that interact with server ---")
(re-frame/reg-event-fx
  ::create-message
  (fn [_world [_ content recipient sender]]
      {:http-xhrio {:method          :post
                    :uri             (str cfg/server-url "/message/")
                    :params          (filter-blank {:content   content
                                                    :recipient recipient
                                                    :sender    sender})
                    :timeout         5000
                    :format          (ajax/json-request-format)
                    :response-format (ajax/json-response-format {:keywords? true})
                    :on-success      [::message-created]
                    :on-failure      [::request-failed]}}))

(re-frame/reg-event-fx
  ::message-created
  (fn [_ [_ response]]
      (js/alert (str "Message with id " (:id response) " has been created!"))))

(re-frame/reg-event-fx
  ::request-failed
  (fn [db [_ response]]
      (comment "This is really lousy error handling ¯\\_(ツ)_/¯")
      (js/alert (str "Request failed" (:response response)))))

(re-frame/reg-event-fx
  ::delete-message
  (fn [_ [_ message-id]]
      {:http-xhrio {:method :delete
                    :uri (str cfg/server-url "/message/" message-id "/")
                    :format          (ajax/json-request-format)
                    :response-format (ajax/json-response-format {:keywords? true})
                    :on-success (re-frame/dispatch [::remove-message message-id])
                    :on-failure [::request-failed]}}))

(re-frame/reg-event-fx
  ::view-new-messages
  (fn [_ _]
      (println "Getting the cow!")
      {:http-xhrio {:method :post
                    :uri (str cfg/server-url "/message/new/")
                    :params {}
                    :format          (ajax/json-request-format)
                    :response-format (ajax/json-response-format {:keywords? true})
                    :on-success [::set-messages]
                    :on-failure [::request-failed]}}))


(re-frame/reg-event-fx
  ::view-message-range
  (fn [_ [_ begin_id end_id]]
      (println "Getting the cow!")
      {:http-xhrio {:method :get
                    :uri (str cfg/server-url "/message/range/" begin_id "/" end_id "/")
                    :response-format (ajax/json-response-format {:keywords? true})
                    :on-success [::set-messages]
                    :on-failure [::request-failed]}}))