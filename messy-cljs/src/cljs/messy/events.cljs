(ns messy.events
  (:require
    [re-frame.core :as re-frame]
    [day8.re-frame.http-fx]
    [ajax.core :as ajax]
    [clojure.string :as str]
    [messy.db :as db]
    [messy.config :as cfg]
    ))

(re-frame/reg-event-db
  ::initialize-db
  (fn [_ _]
      db/default-db))

(re-frame/reg-event-db
  ::set-username
  (fn [db [_ value]]
      (assoc db :username value)))

(defn filter-blank [map]
      (into {} (filter #(seq (second %)) map)))

(re-frame/reg-event-fx
  ::create-message
  (fn [_world [_ content recipient sender]]
      (println content)
      (println recipient)
      (println sender)
      {:http-xhrio {:method          :post
                    :uri             (str cfg/server-url "/message/")
                    :params          (filter-blank {:content   content
                                                    :recipient recipient
                                                    :sender    sender})
                    :timeout         5000
                    :format          (ajax/json-request-format)
                    :response-format (ajax/json-response-format {:keywords? true})
                    :on-success      [::message-created]
                    :on-failure      [::message-failed]}}))

(re-frame/reg-event-db
  ::message-created
  (fn [db [_ response]]
      db))

(re-frame/reg-event-db
  ::message-failed
  (fn [db [_ response]]
      db))